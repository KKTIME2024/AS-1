from flask import render_template, request, redirect, url_for, flash
from app import app, db
from forms import Income, Expenditure, Goal


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incomes')
def incomes():
    items = Income.query.order_by(Income.date_created.desc()).all()
    return render_template('incomes.html', incomes=items)


@app.route('/expenditures')
def expenditures():
    items = Expenditure.query.order_by(Expenditure.date_created.desc()).all()
    return render_template('expenditures.html', expenditures=items)


@app.route('/goals')
def goals():
    items = Goal.query.order_by(Goal.date_created.desc()).all()
    return render_template('goal.html', goals=items)
