from flask_sqlalchemy import SQLAlchemy # 导入 SQLAlchemy
from datetime import datetime # 导入 datetime 用于时间戳

db = SQLAlchemy() 

class Income(db.Model):    
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) # 收入名称不能为空
    amount = db.Column(db.Float, nullable=False) # 收入金额不能为空
    date_added = db.Column(db.DateTime, default=datetime.utcnow) # 自动设置添加时间
    
    def __repr__(self): # 返回字符串表示    
        return f'<Income {self.name} - {self.amount}>'  #返回名称和金额

class Expenditure(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expenditure {self.name} - {self.amount}>'

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)
    target_amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Goal {self.name}>'