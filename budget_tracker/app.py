from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Income, Expenditure, Goal
from forms import TransactionForm, GoalForm

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your-secret-key-here' # 设置密钥以启用会话和闪存消息
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db' # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 禁用跟踪修改以节省资源

db.init_app(app)

@app.route('/') #定义了一个路由，处理主页请求，支持GET方法
def index(): 
    """主页显示统计信息"""
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0 #防止数据库中没有记录时返回 None
    total_expenditure = db.session.query(db.func.sum(Expenditure.amount)).scalar() or 0
    balance = total_income - total_expenditure
    
    goal = Goal.query.first()  
    progress = 0
    if goal and balance > 0:
        progress = (balance / goal.target_amount) * 100 # 计算进度百分比
    
    return render_template('index.html',  
                         total_income=total_income,
                         total_expenditure=total_expenditure,
                         balance=balance,
                         goal=goal,
                         progress=progress) #render_template：Flask中用于渲染HTML模板的函数，将变量传递给模板以动态生成内容


@app.route('/add-transaction', methods=['GET', 'POST']) #定义一个路由处理添加交易记录的请求，支持GET和POST方法
def add_transaction():
    """添加收入/支出"""
    form = TransactionForm() #创建交易表单实例，用户可以输入交易的名称、金额和类型
    
    if form.validate_on_submit(): 
        try:
            if form.type.data == 'income':
                transaction = Income(name=form.name.data, amount=form.amount.data)
            else:
                transaction = Expenditure(name=form.name.data, amount=form.amount.data)
            
            db.session.add(transaction)
            db.session.commit()
            flash('添加成功!', 'success')
            return redirect(url_for('transactions')) #重定向到交易记录页面
            
        except Exception as e:
            db.session.rollback()
            flash('添加失败!', 'error')
    
    return render_template('add_transaction.html', form=form)

@app.route('/transactions') #定义一个路由处理显示交易记录的请求
def transactions():
    """显示所有交易记录"""
    incomes = Income.query.all()
    expenditures = Expenditure.query.all()
    return render_template('transactions.html', 
                         incomes=incomes, 
                         expenditures=expenditures)

@app.route('/edit-transaction/<type>/<int:id>', methods=['GET', 'POST']) #定义一个路由处理编辑交易记录的请求
def edit_transaction(type, id):
    """编辑交易记录"""
    if type == 'income':
        transaction = Income.query.get_or_404(id) 
    else:
        transaction = Expenditure.query.get_or_404(id)
    
    form = TransactionForm(obj=transaction) #创建交易表单实例，预填充现有数据
    form.type.data = type
    
    if form.validate_on_submit():
        transaction.name = form.name.data
        transaction.amount = form.amount.data
        db.session.commit()
        flash('更新成功!', 'success')
        return redirect(url_for('transactions'))
    
    return render_template('edit_transaction.html', form=form, transaction=transaction)

@app.route('/delete-transaction/<type>/<int:id>')
def delete_transaction(type, id):
    """删除交易记录"""
    if type == 'income':
        transaction = Income.query.get_or_404(id)
    else:
        transaction = Expenditure.query.get_or_404(id)
    
    db.session.delete(transaction)
    db.session.commit()
    flash('删除成功!', 'success')
    return redirect(url_for('transactions'))

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    """目标管理"""
    goal = Goal.query.first()
    form = GoalForm() 
    
    if form.validate_on_submit(): 
        if goal:
            goal.name = form.name.data
            goal.target_amount = form.amount.data
        else:
            goal = Goal(name=form.name.data, target_amount=form.amount.data)
            db.session.add(goal) #添加新的目标记录
        
        db.session.commit()
        flash('目标设置成功!', 'success')
        return redirect(url_for('index'))
    
    if goal:
        form.name.data = goal.name
        form.amount.data = goal.target_amount
    
    return render_template('goals.html', form=form, goal=goal)

@app.route('/delete-goal')
def delete_goal():
    """删除目标"""
    goal = Goal.query.first()
    if goal:
        db.session.delete(goal)
        db.session.commit()
        flash('目标已删除!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)#启动 Flask 开发服务器，启用调试模式