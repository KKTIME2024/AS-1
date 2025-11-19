from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, flash
from models import Income, Expense, Goal
from routes import register_routes  # 导入注册路由的函数

db = SQLAlchemy() 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # 初始化数据库

    # 注册路由，传入db实例
    register_routes(app, db)

    return app

app = create_app()

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
