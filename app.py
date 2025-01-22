from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import random
import os
from models import db, User, Question, TestResult
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # 请更改为一个安全的密钥

# 获取当前文件所在目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 确保 instance 文件夹存在
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# 设置数据库路径（使用绝对路径）
db_path = os.path.join(instance_path, 'iq_test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)

# 创建所有表
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    # 获取最近的测试记录
    recent_results = TestResult.query.filter_by(user_id=current_user.id)\
        .order_by(TestResult.completed_at.desc())\
        .limit(5)\
        .all()
    
    return render_template('home.html', 
                         recent_results=recent_results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('两次输入的密码不一致')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/start_test/<test_type>')
@login_required
def start_test(test_type):
    # 根据测试类型设置题目数量和时间限制
    if test_type == 'premium':
        total_questions = 80
        time_limit = 90 * 60  # 90分钟，转换为秒
    else:  # 普通测试
        total_questions = 40
        time_limit = 60 * 60  # 60分钟，转换为秒
    
    # 按难度获取题目
    easy_questions = Question.query.filter_by(difficulty=1).all()
    medium_questions = Question.query.filter_by(difficulty=2).all()
    hard_questions = Question.query.filter_by(difficulty=3).all()
    
    # 计算各难度题目数量
    easy_count = int(total_questions * 0.3)  # 30%
    medium_count = int(total_questions * 0.4)  # 40%
    hard_count = total_questions - easy_count - medium_count  # 剩余题目
    
    # 检查每个难度是否有足够的题目
    if (len(easy_questions) < easy_count or 
        len(medium_questions) < medium_count or 
        len(hard_questions) < hard_count):
        flash('题库中题目数量不足，请联系管理员添加题目。', 'error')
        return redirect(url_for('home'))
    
    # 随机选择指定数量的题目
    selected_questions = []
    selected_questions.extend(random.sample(easy_questions, easy_count))
    selected_questions.extend(random.sample(medium_questions, medium_count))
    selected_questions.extend(random.sample(hard_questions, hard_count))
    
    # 打乱题目顺序
    random.shuffle(selected_questions)
    
    # 存储测试信息到session
    session['questions'] = [q.id for q in selected_questions]
    session['current_question'] = 0
    session['start_time'] = datetime.now().isoformat()
    session['test_type'] = test_type
    session['time_limit'] = time_limit  # 存储总时间限制
    session['remaining_time'] = time_limit  # 初始化剩余时间
    
    # 获取第一个题目
    first_question = selected_questions[0]
    
    return render_template('test.html',
                         question=first_question,
                         current_question_index=0,
                         total_questions=total_questions,
                         questions=session['questions'])  # 将questions传递给模板

@app.route('/test/<int:question_id>')
@login_required
def test(question_id):
    if 'questions' not in session:
        return redirect(url_for('home'))
    
    questions = session['questions']
    
    # 获取当前题目的索引
    current_index = questions.index(question_id)
    
    # 确保当前索引在有效范围内
    if current_index < 0 or current_index >= len(questions):
        return redirect(url_for('test_result'))
    
    current_question = Question.query.get(questions[current_index])
    
    return render_template('test.html',
                           question=current_question,
                           current_question_index=current_index,
                           total_questions=len(questions),
                           questions=questions)  # 确保传递questions

@app.route('/test_result')
@login_required
def test_result():
    if 'answers' not in session or 'start_time' not in session:
        return redirect(url_for('home'))
    
    answers = session.get('answers', [])
    start_time = datetime.fromisoformat(session['start_time'])
    time_spent = (datetime.now() - start_time).total_seconds()
    test_type = session.get('test_type', 'normal')
    
    # 计算得分
    correct_count = sum(1 for answer in answers if answer['correct'])
    total_questions = len(answers)
    
    # 计算IQ分数
    test_result = TestResult(
        user_id=current_user.id,
        test_type=test_type,
        correct_count=correct_count,
        total_questions=total_questions,
        time_spent=int(time_spent),
        answers=json.dumps(answers)
    )
    
    # 计算IQ分数
    test_result.iq_score = test_result.calculate_iq_score()
    
    # 保存到数据库
    db.session.add(test_result)
    db.session.commit()
    
    # 清除session数据
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('start_time', None)
    session.pop('answers', None)
    session.pop('test_type', None)
    
    return render_template('result.html',
                         correct_count=correct_count,
                         total_questions=total_questions,
                         time_spent=f"{time_spent/60:.1f}",
                         iq_score=test_result.iq_score)

@app.route('/test_detail/<int:test_id>')
@login_required
def test_detail(test_id):
    try:
        result = TestResult.query.get_or_404(test_id)
        if result.user_id != current_user.id:
            abort(403)
        
        # 添加错误处理
        answers = []
        try:
            answers = json.loads(result.answers) if result.answers else []
        except json.JSONDecodeError:
            answers = []
            
        total_questions = len(answers)
        if total_questions == 0:
            return jsonify({
                'date': result.completed_at.strftime('%Y-%m-%d %H:%M'),
                'type': '精准测试' if getattr(result, 'test_type', '') == 'premium' else '普通测试',
                'time_spent': round(result.time_spent / 60),
                'accuracy': 0,
                'iq_score': result.iq_score,
                'logical_score': 0,
                'spatial_score': 0,
                'memory_score': 0
            })
            
        # 计算各项能力得分
        logical_correct = sum(1 for a in answers if a['type'] == 'logical' and a['correct'])
        spatial_correct = sum(1 for a in answers if a['type'] == 'spatial' and a['correct'])
        memory_correct = sum(1 for a in answers if a['type'] == 'memory' and a['correct'])
        
        logical_total = sum(1 for a in answers if a['type'] == 'logical')
        spatial_total = sum(1 for a in answers if a['type'] == 'spatial')
        memory_total = sum(1 for a in answers if a['type'] == 'memory')
        
        detail_data = {
            'date': result.completed_at.strftime('%Y-%m-%d %H:%M'),
            'type': '精准测试' if result.test_type == 'premium' else '普通测试',
            'time_spent': round(result.time_spent / 60),
            'accuracy': round(result.correct_count / total_questions * 100),
            'iq_score': result.iq_score,
            'logical_score': round(logical_correct / logical_total * 100) if logical_total > 0 else 0,
            'spatial_score': round(spatial_correct / spatial_total * 100) if spatial_total > 0 else 0,
            'memory_score': round(memory_correct / memory_total * 100) if memory_total > 0 else 0
        }
        
        return jsonify(detail_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profile')
@login_required
def profile():
    # 获取用户的测试历史
    test_results = TestResult.query.filter_by(user_id=current_user.id)\
        .order_by(TestResult.completed_at.desc()).all()
    
    # 计算统计数据
    total_tests = len(test_results)
    avg_iq = round(sum(result.iq_score for result in test_results) / total_tests) if total_tests > 0 else 0
    
    return render_template('profile.html',
                         test_results=test_results,
                         total_tests=total_tests,
                         avg_iq=avg_iq)

@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    if 'questions' not in session:
        return redirect(url_for('home'))
    
    questions = session['questions']
    current_index = session.get('current_question', 0)
    
    if current_index >= len(questions):
        return redirect(url_for('test_result'))
    
    current_question = Question.query.get(questions[current_index])
    if not current_question:
        return redirect(url_for('home'))
    
    # 获取用户答案
    answer = request.form.get('answer')
    if answer is not None:
        # 解析题目数据
        question_data = json.loads(current_question.question_data)
        correct = int(answer) == question_data['correct_index']
        
        # 保存答案
        session['answers'] = session.get('answers', [])
        session['answers'].append({
            'question_id': current_question.id,
            'correct': correct,
            'type': current_question.question_type
        })
        
        # 更新剩余时间
        time_spent = (datetime.now() - datetime.fromisoformat(session['start_time'])).total_seconds()
        remaining_time = session['time_limit'] - time_spent
        session['remaining_time'] = max(0, remaining_time)  # 确保不为负数
        
        # 移动到下一题
        session['current_question'] = current_index + 1
        
        if current_index + 1 >= len(questions):
            return redirect(url_for('test_result'))
    
    return redirect(url_for('test', question_id=questions[current_index + 1]))

@app.template_filter('from_json')
def from_json(value):
    return json.loads(value)

# 添加上下文处理器
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
