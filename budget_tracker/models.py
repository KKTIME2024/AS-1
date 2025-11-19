from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # 初始化 db

class Income(db.Model):
    """收入数据模型 - 移除了名称唯一性约束"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 移除了 unique=True
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)  # 新增描述字段，可选
    
    def __repr__(self):
        return f'Income(name="{self.name}", amount={self.amount}, date={self.created_at.date()})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class Expense(db.Model):
    """支出数据模型 - 移除了名称唯一性约束"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 移除了 unique=True
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)  # 新增描述字段，可选
    category = db.Column(db.String(50), nullable=True)  # 新增分类字段，可选
    
    def __repr__(self):
        return f'Expense(name="{self.name}", amount={self.amount}, date={self.created_at.date()})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }

class Goal(db.Model):
    """储蓄目标数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    target_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Goal(name="{self.name}", target_amount={self.target_amount})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'target_amount': self.target_amount,
            'created_at': self.created_at.isoformat()
        }
