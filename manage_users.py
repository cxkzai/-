from app import app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_users():
    with app.app_context():
        # 清空现有用户表
        User.query.delete()
        
        # 创建默认用户列表
        default_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'is_premium': True,
                'created_at': datetime.utcnow()
            },
            {
                'username': 'test',
                'password': 'test123',
                'is_premium': False,
                'created_at': datetime.utcnow()
            }
        ]
        
        # 添加用户到数据库
        for user_data in default_users:
            user = User(
                username=user_data['username'],
                password_hash=generate_password_hash(user_data['password']),
                is_premium=user_data['is_premium'],
                created_at=user_data['created_at']
            )
            db.session.add(user)
        
        # 提交更改
        db.session.commit()
        print("默认用户创建完成！")

def list_users():
    with app.app_context():
        users = User.query.all()
        print("\n当前用户列表：")
        print("-" * 50)
        print(f"{'用户名':<15} {'注册时间':<20} {'会员状态':<10}")
        print("-" * 50)
        for user in users:
            print(f"{user.username:<15} {user.created_at.strftime('%Y-%m-%d %H:%M'):<20} {'是' if user.is_premium else '否':<10}")

def add_user(username, password, is_premium=False):
    with app.app_context():
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            print(f"用户名 {username} 已存在！")
            return False
        
        # 创建新用户
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            is_premium=is_premium,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        print(f"用户 {username} 创建成功！")
        return True

def delete_user(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"用户 {username} 删除成功！")
        else:
            print(f"用户 {username} 不存在！")

def change_password(username, new_password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            print(f"用户 {username} 密码修改成功！")
        else:
            print(f"用户 {username} 不存在！")

if __name__ == "__main__":
    while True:
        print("\n用户管理系统")
        print("1. 初始化默认用户")
        print("2. 查看所有用户")
        print("3. 添加新用户")
        print("4. 删除用户")
        print("5. 修改用户密码")
        print("0. 退出")
        
        choice = input("请选择操作 (0-5): ")
        
        if choice == "1":
            init_users()
        elif choice == "2":
            list_users()
        elif choice == "3":
            username = input("请输入用户名: ")
            password = input("请输入密码: ")
            is_premium = input("是否为会员 (y/n): ").lower() == 'y'
            add_user(username, password, is_premium)
        elif choice == "4":
            username = input("请输入要删除的用户名: ")
            delete_user(username)
        elif choice == "5":
            username = input("请输入用户名: ")
            new_password = input("请输入新密码: ")
            confirm_password = input("请确认新密码: ")
            if new_password == confirm_password:
                change_password(username, new_password)
            else:
                print("两次输入的密码不一致！")
        elif choice == "0":
            break
        else:
            print("无效的选择，请重试！") 