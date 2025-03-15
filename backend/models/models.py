from datetime import datetime
from extensions import db

        
class Events(db.Model):
    __tablename__="events"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255),nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_bill = db.Column(db.Numeric(10, 2), nullable=True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    update_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%d-%m-%Y") if self.date else None,
            "total_bill": float(self.total_bill) if self.total_bill is not None else None, # vì json không hỗ trọ numeric của postgres
            "created_at": self.created_at.strftime("%H:%M:%S %d-%m-%Y") if self.created_at else None,
            "update_at": self.update_at.strftime("%H:%M:%S %d-%m-%Y") if self.update_at else None,
        }      

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email_teams = db.Column(db.String(255),nullable = False)
    sdt = db.Column(db.String(255), nullable = False)
    ten_nh = db.Column(db.String(255),nullable = False)
    stk = db.Column(db.String(50),nullable = False)
    created_at= db.Column(db.DateTime, default = datetime.utcnow)
    update_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "email_teams": self.email_teams,
            "sdt": self.sdt,
            "ten_nh": self.ten_nh,
            "stk": self.stk,
            "created_at": self.created_at.strftime('%H:%M:%S %Y-%m-%d'),
            "update_at": self.update_at.strftime('%H:%M:%S %Y-%m-%d')
        }