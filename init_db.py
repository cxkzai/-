from app import db, app

with app.app_context():
    # 删除所有表
    db.drop_all()
    # 创建所有表
    db.create_all()
    print("数据库已重新初始化！")
