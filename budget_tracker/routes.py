# @author:JK
from flask import render_template, redirect, url_for, request, flash
import sys
import os

# Add the current directory to Python path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def register_routes(app, db):
    # 确保所有模型使用同一个db实例
    # 这里我们需要在应用上下文中导入模型
    
    # 首页路由
    @app.route('/')
    def index():
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Income, Expense, Goal
            
            # 获取财务概览数据
            # 查询所有收入和支出记录
            incomes = Income.query.all()
            expenses = Expense.query.all()
            goals = Goal.query.all()
            
            # 计算总收入和总支出
            total_income = sum(income.amount for income in incomes)
            total_expense = sum(expense.amount for expense in expenses)
            available_savings = total_income - total_expense
            
            # 转换目标为字典格式并计算进度
            goals_data = []
            for goal in goals:
                # 计算每个目标的进度百分比
                progress = 0
                if goal.target_amount > 0:
                    progress = max(0, min(100, (available_savings / goal.target_amount) * 100))
                
                goals_data.append({
                    'id': goal.id,
                    'name': goal.name,
                    'target_amount': goal.target_amount,
                    'current_amount': available_savings,
                    'progress_percentage': progress
                })
            
            # 按标签分类统计收入
            income_by_category = {}
            for income in incomes:
                category = income.category or '未分类'
                if category not in income_by_category:
                    income_by_category[category] = 0
                income_by_category[category] += income.amount
            
            # 按标签分类统计支出
            expense_by_category = {}
            for expense in expenses:
                category = expense.category or '未分类'
                if category not in expense_by_category:
                    expense_by_category[category] = 0
                expense_by_category[category] += expense.amount
            
            # 转换为图表可用的数据格式
            income_categories = []
            income_amounts = []
            for category, amount in income_by_category.items():
                income_categories.append(category)
                income_amounts.append(amount)
            
            expense_categories = []
            expense_amounts = []
            for category, amount in expense_by_category.items():
                expense_categories.append(category)
                expense_amounts.append(amount)
            
            # 准备图表数据
            chart_data = {
                'total_income': total_income,
                'total_expense': total_expense,
                'available_savings': available_savings,
                'goals': goals_data,
                'income_categories': income_categories,
                'income_amounts': income_amounts,
                'expense_categories': expense_categories,
                'expense_amounts': expense_amounts
            }
            
            return render_template('index.html', chart_data=chart_data)
    
    # 收入管理页面路由
    @app.route('/incomes')
    def incomes():
        return render_template('incomes.html')
    
    # 添加收入路由
    @app.route('/add_income', methods=['POST'])
    def add_income():
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Income
            name = request.form['name']
            
            # 服务器端数据验证
            try:
                amount = float(request.form['amount'])
                # 验证金额必须大于0
                if amount <= 0:
                    flash('错误：收入金额必须大于0！', 'error')
                    return redirect(url_for('incomes'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('incomes'))
                
            description = request.form.get('description', '')
            category = request.form.get('category', '')
            new_income = Income(name=name, amount=amount, description=description, category=category)
            db.session.add(new_income)
            db.session.commit()
            flash('收入添加成功！', 'success')
        return redirect(url_for('incomes'))
    
    # 支出管理页面路由
    @app.route('/expenditures')
    def expenditures():
        return render_template('expenditures.html')
    
    # 添加支出路由
    @app.route('/add_expenditure', methods=['POST'])
    def add_expenditure():
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Expense
            name = request.form['name']
            
            # 服务器端数据验证
            try:
                amount = float(request.form['amount'])
                # 验证金额必须大于0
                if amount <= 0:
                    flash('错误：支出金额必须大于0！', 'error')
                    return redirect(url_for('expenditures'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('expenditures'))
                
            description = request.form.get('description', '')
            category = request.form.get('category', '')
            new_expenditure = Expense(name=name, amount=amount, description=description, category=category)
            db.session.add(new_expenditure)
            db.session.commit()
            flash('支出添加成功！', 'success')
        return redirect(url_for('expenditures'))
    
    # 目标页面路由
    @app.route('/goal')
    def goal():
        with app.app_context():
            from models import Goal, Income, Expense
            # 查询所有目标
            goals = Goal.query.all()
            # 查询所有收入和支出记录以计算可用储蓄
            incomes = Income.query.all()
            expenses = Expense.query.all()
            
            # 计算总收入和总支出
            total_income = sum(income.amount for income in incomes)
            total_expense = sum(expense.amount for expense in expenses)
            
            # 计算可用储蓄金额（收入减去支出）
            available_savings = total_income - total_expense
            
            # 转换目标为字典格式
            goals_dict = [goal.to_dict() for goal in goals]
            
            # 计算每个目标的进度百分比，使用可用储蓄作为当前金额
            for g in goals_dict:
                # 使用实际储蓄金额作为当前进度
                g['current_amount'] = available_savings
                if g['target_amount'] > 0:
                    # 计算进度百分比，但确保不小于0且不大于100
                    progress = (available_savings / g['target_amount']) * 100
                    g['progress_percentage'] = max(0, min(100, progress))
                else:
                    g['progress_percentage'] = 0
                    
            # 将总览信息也传递给模板
            overview = {
                'total_income': total_income,
                'total_expense': total_expense,
                'available_savings': available_savings
            }
            
            return render_template('goal.html', goals=goals_dict, overview=overview)
    
    # 添加储蓄目标路由
    @app.route('/add_goal', methods=['POST'])
    def add_goal():
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Goal
            from datetime import datetime
            
            # 获取表单数据
            name = request.form.get('name', '未命名目标')
            
            # 服务器端数据验证
            try:
                target_amount = float(request.form['target_amount'])
                # 验证金额必须大于0
                if target_amount <= 0:
                    flash('错误：目标金额必须大于0！', 'error')
                    return redirect(url_for('goal'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('goal'))
            
            description = request.form.get('description', '')
            
            # 创建新目标
            new_goal = Goal(
                name=name,
                target_amount=target_amount,
                current_amount=0.0,  # 初始金额为0
                description=description
            )
            
            db.session.add(new_goal)
            db.session.commit()
            flash('储蓄目标添加成功！', 'success')
        return redirect(url_for('goal'))
    
    # 编辑储蓄目标路由
    @app.route('/edit_goal/<int:goal_id>', methods=['POST'])
    def edit_goal(goal_id):
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Goal
            
            # 通过主键查找目标
            goal = Goal.query.get(goal_id)
            if not goal:
                flash('错误：未找到该目标！', 'error')
                return redirect(url_for('goal'))
            
            # 获取表单数据并更新目标
            name = request.form.get('name', '未命名目标')
            
            # 服务器端数据验证
            try:
                target_amount = float(request.form['target_amount'])
                # 验证金额必须大于0
                if target_amount <= 0:
                    flash('错误：目标金额必须大于0！', 'error')
                    return redirect(url_for('goal'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('goal'))
            
            description = request.form.get('description', '')
            
            # 更新目标信息
            goal.name = name
            goal.target_amount = target_amount
            goal.description = description
            
            db.session.commit()
            flash('储蓄目标更新成功！', 'success')
        return redirect(url_for('goal'))
    
    # 删除储蓄目标路由
    @app.route('/delete_goal/<int:goal_id>', methods=['POST'])
    def delete_goal(goal_id):
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Goal
            
            # 通过主键查找目标
            goal = Goal.query.get(goal_id)
            if not goal:
                flash('错误：未找到该目标！', 'error')
                return redirect(url_for('goal'))
            
            # 删除目标
            db.session.delete(goal)
            db.session.commit()
            flash('储蓄目标删除成功！', 'success')
        return redirect(url_for('goal'))
    
    # 交易记录页面路由 - GET请求直接显示所有记录
    @app.route('/transaction')
    def transaction():
        with app.app_context():
            # 在应用上下文中导入模型并执行查询
            from models import Income, Expense
            # 查询所有收入和支出记录
            incomes = Income.query.all()
            expenditures = Expense.query.all()
            # 转换为字典格式
            incomes_dict = [income.to_dict() for income in incomes]
            expenditures_dict = [expenditure.to_dict() for expenditure in expenditures]
            # 渲染模板并传递数据
            return render_template('transaction.html', incomes=incomes_dict, expenditures=expenditures_dict)
    
    # 编辑收入记录路由
    @app.route('/edit_income/<int:income_id>', methods=['POST'])
    def edit_income(income_id):
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Income
            
            # 通过主键查找收入记录
            income = Income.query.get(income_id)
            if not income:
                flash('错误：未找到该收入记录！', 'error')
                return redirect(url_for('transaction'))
            
            # 获取表单数据并更新收入记录
            name = request.form['name']
            
            # 服务器端数据验证
            try:
                amount = float(request.form['amount'])
                # 验证金额必须大于0
                if amount <= 0:
                    flash('错误：收入金额必须大于0！', 'error')
                    return redirect(url_for('transaction'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('transaction'))
            
            description = request.form.get('description', '')
            
            # 更新收入记录信息
            income.name = name
            income.amount = amount
            income.description = description
            
            db.session.commit()
            flash('收入记录更新成功！', 'success')
        return redirect(url_for('transaction'))
    
    # 编辑支出记录路由
    @app.route('/edit_expenditure/<int:expenditure_id>', methods=['POST'])
    def edit_expenditure(expenditure_id):
        with app.app_context():
            # 在应用上下文中导入模型
            from models import Expense
            
            # 通过主键查找支出记录
            expense = Expense.query.get(expenditure_id)
            if not expense:
                flash('错误：未找到该支出记录！', 'error')
                return redirect(url_for('transaction'))
            
            # 获取表单数据并更新支出记录
            name = request.form['name']
            
            # 服务器端数据验证
            try:
                amount = float(request.form['amount'])
                # 验证金额必须大于0
                if amount <= 0:
                    flash('错误：支出金额必须大于0！', 'error')
                    return redirect(url_for('transaction'))
            except ValueError:
                flash('错误：请输入有效的金额数值！', 'error')
                return redirect(url_for('transaction'))
            
            category = request.form.get('category', '')
            description = request.form.get('description', '')
            
            # 更新支出记录信息
            expense.name = name
            expense.amount = amount
            expense.category = category
            expense.description = description
            
            db.session.commit()
            flash('支出记录更新成功！', 'success')
        return redirect(url_for('transaction'))