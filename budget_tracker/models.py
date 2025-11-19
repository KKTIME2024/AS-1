from datetime import datetime

# 使用延迟导入避免循环依赖问题
# 这个模块将在应用上下文中被导入，此时db实例已经被正确初始化

# 定义模型但不立即使用db，因为db将在应用上下文中提供
class Income:
    """收入数据模型 - 移除了名称唯一性约束"""
    # 注意：这些定义只是类型提示，实际的db.Column将在运行时由SQLAlchemy处理
    id = None
    name = None
    amount = None
    created_at = None
    description = None
    
    def __repr__(self):
        return f'Income(name="{self.name}", amount={self.amount}, date={self.created_at.date()})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Expense:
    """支出数据模型"""
    # 注意：这些定义只是类型提示，实际的db.Column将在运行时由SQLAlchemy处理
    id = None
    name = None
    amount = None
    category = None
    created_at = None
    description = None
    
    def __repr__(self):
        return f'Expense(name="{self.name}", amount={self.amount}, category={self.category}, date={self.created_at.date()})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'description': self.description
        }

class Goal:
    """财务目标数据模型"""
    # 注意：这些定义只是类型提示，实际的db.Column将在运行时由SQLAlchemy处理
    id = None
    name = None
    target_amount = None
    current_amount = None
    deadline = None
    created_at = None
    description = None
    
    def __repr__(self):
        return f'Goal(name="{self.name}", target={self.target_amount}, current={self.current_amount})'
    
    def to_dict(self):
        """将模型转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'description': self.description
        }

# 这个函数会在应用初始化时调用，用于正确设置模型与db的关系
def setup_models(db_instance):
    """设置模型与数据库实例的关系"""
    global Income, Expense, Goal
    
    # 重新定义模型，使用传入的db实例
    class Income(db_instance.Model):
        """收入数据模型 - 移除了名称唯一性约束"""
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        name = db_instance.Column(db_instance.String(100), nullable=False)
        amount = db_instance.Column(db_instance.Float, nullable=False)
        created_at = db_instance.Column(db_instance.DateTime, default=datetime.utcnow)
        description = db_instance.Column(db_instance.Text, nullable=True)
        
        def __repr__(self):
            return f'Income(name="{self.name}", amount={self.amount}, date={self.created_at.date()})'
        
        def to_dict(self):
            """将模型转换为字典格式"""
            return {
                'id': self.id,
                'name': self.name,
                'amount': self.amount,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'description': self.description
            }
    
    class Expense(db_instance.Model):
        """支出数据模型"""
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        name = db_instance.Column(db_instance.String(100), nullable=False)
        amount = db_instance.Column(db_instance.Float, nullable=False)
        category = db_instance.Column(db_instance.String(50), nullable=True)
        created_at = db_instance.Column(db_instance.DateTime, default=datetime.utcnow)
        description = db_instance.Column(db_instance.Text, nullable=True)
        
        def __repr__(self):
            return f'Expense(name="{self.name}", amount={self.amount}, category={self.category}, date={self.created_at.date()})'
        
        def to_dict(self):
            """将模型转换为字典格式"""
            return {
                'id': self.id,
                'name': self.name,
                'amount': self.amount,
                'category': self.category,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'description': self.description
            }
    
    class Goal(db_instance.Model):
        """财务目标数据模型"""
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        name = db_instance.Column(db_instance.String(100), nullable=False)
        target_amount = db_instance.Column(db_instance.Float, nullable=False)
        current_amount = db_instance.Column(db_instance.Float, default=0.0)
        deadline = db_instance.Column(db_instance.Date, nullable=True)
        created_at = db_instance.Column(db_instance.DateTime, default=datetime.utcnow)
        description = db_instance.Column(db_instance.Text, nullable=True)
        
        def __repr__(self):
            return f'Goal(name="{self.name}", target={self.target_amount}, current={self.current_amount})'
        
        def to_dict(self):
            """将模型转换为字典格式"""
            return {
                'id': self.id,
                'name': self.name,
                'target_amount': self.target_amount,
                'current_amount': self.current_amount,
                'deadline': self.deadline.isoformat() if self.deadline else None,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'description': self.description
            }
    
    return Income, Expense, Goal
