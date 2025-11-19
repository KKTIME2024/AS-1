from flask import render_template, redirect, url_for, request, flash
from models import Income, Expense, Goal

def register_routes(app, db):
    # db实例作为参数传入，避免循环导入问题

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/incomes')
    def incomes():
        return render_template('incomes.html')

    @app.route('/add_income', methods=['POST'])
    def add_income():
        # 使用通过register_routes传入的db实例
        name = request.form['name']
        amount = float(request.form['amount'])
        description = request.form['description']
        new_income = Income(name=name, amount=amount, description=description)
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('incomes'))

    @app.route('/expenditures')
    def expenditures():
        return render_template('expenditures.html')

    @app.route('/goal')
    def goal():
        return render_template('goal.html')

    @app.route('/transaction')
    def transaction():
        return render_template('transaction.html')
