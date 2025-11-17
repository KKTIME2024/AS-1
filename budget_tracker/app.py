from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Income, Expense, Goal
from flask import request, redirect, url_for, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 禁用跟踪修改以节省资源
db = SQLAlchemy(app) # 初始化数据库

@app.route('/')
def index():
    return render_template('index.html')

#收入功能
@app.route('/incomes')
def incomes():
    return render_template('incomes.html')

# 添加收入的路由
@app.route('/add_income', methods=['POST'])
def add_income():
    name = request.form['name']
    amount = float(request.form['amount'])
    description = request.form['description']
    new_income = Income(name=name, amount=amount, description=description)
    db.session.add(new_income)
    db.session.commit()
    return redirect(url_for('incomes'))




#支出功能
@app.route('/expenditures')
def expenditures():
    return render_template('expenditures.html')







#储蓄目标功能
@app.route('/goal')
def goal():
    return render_template('goal.html')







#查看所有收支记录
@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


#运行应用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 初始化数据库
    app.run(debug=True)