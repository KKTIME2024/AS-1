# @author:JK
from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from routes import register_routes

# 首先创建db实例
db = SQLAlchemy()


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
        # 注意：在开发模式下，数据库表会在主函数中被drop_all()和create_all()重新创建

    # 注册路由，传入db实例
    register_routes(app, db)

    return app


app = create_app()

# 运行应用
if __name__ == '__main__':
    # 初始化数据库
    with app.app_context():
        print("使用SQLAlchemy的drop_all()和create_all()方法更新数据库表结构")

        # 关闭所有现有连接
        db.session.close_all()

        try:
            # 首先删除所有表
            print("正在删除所有现有表...")
            db.drop_all()
            print("所有表已成功删除")

            # 然后重新创建所有表
            print("正在创建新的表结构...")
            db.create_all()
            print("所有表已成功创建")
            print("Goal表现在应该包含current_amount字段")
        except Exception as e:
            print(f"更新数据库表结构时出错: {e}")

    app.run(debug=True)
