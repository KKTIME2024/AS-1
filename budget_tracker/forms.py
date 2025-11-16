from flask_wtf import FlaskForm 
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class TransactionForm(FlaskForm):
    name = StringField('名称', validators=[
        DataRequired(message='请输入名称'),
        Length(min=2, max=100, message='名称长度应在2-100字符之间')
    ])
    amount = FloatField('金额', validators=[
        DataRequired(message='请输入金额'),
        NumberRange(min=0.01, message='金额必须大于0')
    ])
    type = SelectField('类型', choices=[
        ('income', '收入'),
        ('expenditure', '支出')
    ], validators=[DataRequired()])

class GoalForm(FlaskForm):
    name = StringField('目标名称', validators=[
        Length(max=100, message='名称不能超过100字符')
    ])
    amount = FloatField('目标金额', validators=[
        DataRequired(message='请输入目标金额'),
        NumberRange(min=0.01, message='金额必须大于0')
    ])