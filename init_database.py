from app import app
from models import db, User, Question, TestResult
from datetime import datetime
import random
import math
from werkzeug.security import generate_password_hash
import uuid
import hashlib
import json

def generate_svg(width, height, shapes):
    """生成SVG图形，确保图形在指定范围内"""
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    
    # 计算中心点
    center_x = width / 2
    center_y = height / 2
    
    # 添加背景
    svg += f'<rect width="{width}" height="{height}" fill="white"/>'
    
    for shape in shapes:
        shape_type = shape['type']
        size = shape['size']
        angle = shape.get('angle', 0)
        color = shape.get('color', 'black')
        
        # 确保图形不会超出边界
        max_size = min(width, height) * 0.4  # 限制最大尺寸为容器的40%
        size = min(size, max_size)
        
        # 根据形状类型生成SVG元素
        if shape_type == 'circle':
            svg += f'<circle cx="{center_x}" cy="{center_y}" r="{size/2}" '
            svg += f'fill="{color}" transform="rotate({angle} {center_x} {center_y})"/>'
            
        elif shape_type == 'square':
            x = center_x - size/2
            y = center_y - size/2
            svg += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" '
            svg += f'fill="{color}" transform="rotate({angle} {center_x} {center_y})"/>'
            
        elif shape_type == 'triangle':
            # 计算等边三角形的顶点
            r = size / 2
            points = []
            for i in range(3):
                angle_rad = math.radians(i * 120 + angle)
                px = center_x + r * math.cos(angle_rad)
                py = center_y + r * math.sin(angle_rad)
                points.append(f"{px},{py}")
            svg += f'<polygon points="{" ".join(points)}" fill="{color}"/>'
    
    svg += '</svg>'
    return svg

def generate_number_pattern(difficulty):
    """生成数字规律题目"""
    patterns = {
        1: [  # 简单
            lambda x: x * 2,  # 倍数
            lambda x: x + 5,  # 等差
            lambda x: x ** 2,  # 平方
        ],
        2: [  # 中等
            lambda x: x * 3 - 1,  # 倍数加减
            lambda x: x ** 2 + x,  # 平方加自身
            lambda x: int(x * 1.5) + 2,  # 复合运算
        ],
        3: [  # 困难
            lambda x: int((x ** 2 + x) / 2),  # 复杂公式
            lambda x: int(x * 1.8 + x ** 0.5),  # 开方运算
            lambda x: int(x * math.log(x + 1, 2)),  # 对数运算
        ]
    }
    
    # 选择规律
    pattern_func = random.choice(patterns[difficulty])
    
    # 生成初始数
    if difficulty == 1:
        start = random.randint(2, 10)
    elif difficulty == 2:
        start = random.randint(5, 15)
    else:
        start = random.randint(10, 20)
    
    # 生成序列
    sequence = [start]
    for i in range(3):
        sequence.append(pattern_func(sequence[-1]))
    
    # 生成SVG
    svgs = []
    for num in sequence[:-1]:  # 不包括最后一个数字（答案）
        svg = f'''
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="200" fill="white"/>
            <text x="100" y="100" text-anchor="middle" dominant-baseline="middle" 
                  font-family="Arial" font-size="24" fill="black">
                {num}
            </text>
        </svg>
        '''
        svgs.append(svg)
    
    # 生成选项
    correct_answer = sequence[-1]
    options = [correct_answer]
    
    # 生成干扰选项
    variations = [0.8, 1.2, 1.5]  # 干扰因子
    for var in variations:
        wrong_answer = int(correct_answer * var)
        if wrong_answer == correct_answer:
            wrong_answer += random.randint(1, 5)
        options.append(wrong_answer)
    
    # 为选项生成SVG
    option_svgs = []
    for opt in options:
        svg = f'''
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="200" fill="white"/>
            <text x="100" y="100" text-anchor="middle" dominant-baseline="middle" 
                  font-family="Arial" font-size="24" fill="black">
                {opt}
            </text>
        </svg>
        '''
        option_svgs.append(svg)
    
    return {
        'question_svgs': svgs,
        'options': option_svgs,
        'correct_index': 0  # 因为正确答案在第一个位置
    }

def generate_shape_pattern(difficulty):
    """生成图形规律题目"""
    width = 200
    height = 200
    
    # 基础形状和变换
    shapes = ['circle', 'rect', 'polygon']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    # 根据难度设置参数
    if difficulty == 1:  # 简单
        num_shapes = 1
        size_range = (40, 60)
        angle_step = 45
    elif difficulty == 2:  # 中等
        num_shapes = 2
        size_range = (30, 50)
        angle_step = 60
    else:  # 困难
        num_shapes = 3
        size_range = (25, 40)
        angle_step = 90
    
    # 生成基础形状
    base_shapes = []
    for _ in range(num_shapes):
        shape = {
            'type': random.choice(shapes),
            'size': random.randint(*size_range),
            'color': random.choice(colors),
            'x': width // 2,
            'y': height // 2
        }
        base_shapes.append(shape)
    
    # 生成序列
    svgs = []
    for i in range(3):  # 生成3个问题图形
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg += f'<rect width="{width}" height="{height}" fill="white"/>'
        
        for shape in base_shapes:
            if shape['type'] == 'circle':
                svg += f'<circle cx="{shape["x"]}" cy="{shape["y"]}" r="{shape["size"]/2}" '
                svg += f'fill="{shape["color"]}" transform="rotate({i*angle_step} {width/2} {height/2})"/>'
            
            elif shape['type'] == 'rect':
                x = shape['x'] - shape['size']/2
                y = shape['y'] - shape['size']/2
                svg += f'<rect x="{x}" y="{y}" width="{shape["size"]}" height="{shape["size"]}" '
                svg += f'fill="{shape["color"]}" transform="rotate({i*angle_step} {width/2} {height/2})"/>'
            
            elif shape['type'] == 'polygon':
                points = []
                r = shape['size'] / 2
                for j in range(3):
                    angle_rad = math.radians(j * 120 + i * angle_step)
                    px = shape['x'] + r * math.cos(angle_rad)
                    py = shape['y'] + r * math.sin(angle_rad)
                    points.append(f"{px},{py}")
                svg += f'<polygon points="{" ".join(points)}" fill="{shape["color"]}"/>'
        
        svg += '</svg>'
        svgs.append(svg)
    
    # 生成选项
    options = []
    
    # 正确答案
    correct_svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    correct_svg += f'<rect width="{width}" height="{height}" fill="white"/>'
    for shape in base_shapes:
        if shape['type'] == 'circle':
            correct_svg += f'<circle cx="{shape["x"]}" cy="{shape["y"]}" r="{shape["size"]/2}" '
            correct_svg += f'fill="{shape["color"]}" transform="rotate({3*angle_step} {width/2} {height/2})"/>'
        elif shape['type'] == 'rect':
            x = shape['x'] - shape['size']/2
            y = shape['y'] - shape['size']/2
            correct_svg += f'<rect x="{x}" y="{y}" width="{shape["size"]}" height="{shape["size"]}" '
            correct_svg += f'fill="{shape["color"]}" transform="rotate({3*angle_step} {width/2} {height/2})"/>'
        elif shape['type'] == 'polygon':
            points = []
            r = shape['size'] / 2
            for j in range(3):
                angle_rad = math.radians(j * 120 + 3 * angle_step)
                px = shape['x'] + r * math.cos(angle_rad)
                py = shape['y'] + r * math.sin(angle_rad)
                points.append(f"{px},{py}")
            correct_svg += f'<polygon points="{" ".join(points)}" fill="{shape["color"]}"/>'
    correct_svg += '</svg>'
    options.append(correct_svg)
    
    # 生成干扰选项
    for i in range(3):
        wrong_svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        wrong_svg += f'<rect width="{width}" height="{height}" fill="white"/>'
        for shape in base_shapes:
            # 使用不同的变化生成干扰选项
            if i == 0:
                angle_mod = 2 * angle_step  # 角度不够
                size_mod = 1
            elif i == 1:
                angle_mod = 4 * angle_step  # 角度过大
                size_mod = 1
            else:
                angle_mod = 3 * angle_step
                size_mod = 1.2  # 尺寸变化
            
            if shape['type'] == 'circle':
                wrong_svg += f'<circle cx="{shape["x"]}" cy="{shape["y"]}" r="{shape["size"]*size_mod/2}" '
                wrong_svg += f'fill="{shape["color"]}" transform="rotate({angle_mod} {width/2} {height/2})"/>'
            elif shape['type'] == 'rect':
                x = shape['x'] - shape['size']*size_mod/2
                y = shape['y'] - shape['size']*size_mod/2
                wrong_svg += f'<rect x="{x}" y="{y}" width="{shape["size"]*size_mod}" height="{shape["size"]*size_mod}" '
                wrong_svg += f'fill="{shape["color"]}" transform="rotate({angle_mod} {width/2} {height/2})"/>'
            elif shape['type'] == 'polygon':
                points = []
                r = shape['size'] * size_mod / 2
                for j in range(3):
                    angle_rad = math.radians(j * 120 + angle_mod)
                    px = shape['x'] + r * math.cos(angle_rad)
                    py = shape['y'] + r * math.sin(angle_rad)
                    points.append(f"{px},{py}")
                wrong_svg += f'<polygon points="{" ".join(points)}" fill="{shape["color"]}"/>'
        wrong_svg += '</svg>'
        options.append(wrong_svg)
    
    # 打乱选项顺序
    random.shuffle(options)
    correct_index = options.index(correct_svg)
    
    return {
        'question_svgs': svgs,
        'options': options,
        'correct_index': correct_index
    }

def generate_svg_question(difficulty):
    """根据难度生成题目，随机选择数字规律或图形规律"""
    # 生成一个唯一的题目ID
    question_id = str(uuid.uuid4())
    
    # 生成题目内容
    if random.random() < 0.5:  # 50%概率生成数字规律题
        result = generate_number_pattern(difficulty)
    else:  # 50%概率生成图形规律题
        result = generate_shape_pattern(difficulty)
    
    # 添加题目ID和类型信息
    result['question_id'] = question_id
    result['type'] = 'number' if 'sequence' in result else 'shape'
    
    return result

def init_db():
    with app.app_context():
        # 删除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()

        # 为每个难度等级生成题目
        questions_per_difficulty = 20  # 每个难度级别生成20道题
        used_patterns = set()  # 用于记录已使用的题目模式

        for difficulty in [1, 2, 3]:  # 1=简单, 2=中等, 3=困难
            questions = []
            attempts = 0
            max_attempts = questions_per_difficulty * 3  # 最大尝试次数，防止无限循环

            while len(questions) < questions_per_difficulty and attempts < max_attempts:
                attempts += 1
                question_data = generate_svg_question(difficulty)
                
                # 生成题目的特征码（用于判断重复）
                pattern_key = str(question_data['question_svgs']) + str(question_data['options'])
                pattern_hash = hashlib.md5(pattern_key.encode()).hexdigest()

                # 如果题目不重复，则添加到列表中
                if pattern_hash not in used_patterns:
                    used_patterns.add(pattern_hash)
                    
                    question = Question(
                        id=question_data['question_id'],
                        difficulty=difficulty,
                        question_type=question_data['type'],
                        question_data=json.dumps({
                            'svgs': question_data['question_svgs'],
                            'options': question_data['options'],
                            'correct_index': question_data['correct_index']
                        }),
                        created_at=datetime.utcnow()
                    )
                    questions.append(question)

            # 添加生成的题目到数据库
            db.session.add_all(questions)
            db.session.commit()

        # 创建默认用户
        user = User(
            username='test',
            password_hash=generate_password_hash('test'),
            date_joined=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    init_db()
