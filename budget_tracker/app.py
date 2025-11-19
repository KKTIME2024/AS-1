from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy

# 首先创建db实例
db = SQLAlchemy() 

# 将models导入移到create_app函数内部以避免循环导入

# 然后导入路由函数
from routes import register_routes  # 导入注册路由的函数
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # 添加SECRET_KEY以启用Flash消息

    db.init_app(app)

    # 在应用上下文中设置模型
    with app.app_context():
        # 导入setup_models函数
        from models import setup_models
        
        # 使用当前的db实例设置模型
        Income, Expense, Goal = setup_models(db)
        
        # 初始化数据库
        db.create_all()

    # 注册路由，传入db实例
    register_routes(app, db)

    return app

app = create_app()

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
