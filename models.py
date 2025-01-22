from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    test_results = db.relationship('TestResult', backref='user', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(20), nullable=False)  # logical, spatial, memory
    difficulty = db.Column(db.Integer, nullable=False)  # 1: 简单, 2: 中等, 3: 困难
    question_data = db.Column(db.Text, nullable=False)  # JSON格式存储题目数据
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # normal, premium
    correct_count = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)  # 以秒为单位
    iq_score = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON格式存储答题记录
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_iq_score(self):
        # 基础分数
        base_score = 100
        
        # 根据正确率调整
        accuracy = self.correct_count / self.total_questions
        accuracy_adjustment = (accuracy - 0.5) * 50  # 50%正确率对应100分
        
        # 根据答题时间调整
        expected_time = 90 * 60 if self.test_type == 'premium' else 60 * 60  # 秒
        time_ratio = self.time_spent / expected_time
        time_adjustment = max(0, (1 - time_ratio) * 10)  # 最多加10分
        
        # 计算最终分数
        final_score = base_score + accuracy_adjustment + time_adjustment
        
        # 限制分数范围在70-150之间
        return max(70, min(150, round(final_score)))
