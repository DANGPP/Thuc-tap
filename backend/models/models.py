from datetime import datetime
from extensions import db

        
class Events(db.Model):
    __tablename__="events"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255),nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_bill = db.Column(db.Integer, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    update_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)
    tong_thu = db.Column(db.Integer, nullable = True)
    tien_thua = db.Column(db.Integer, nullable = True)
    status = db.Column(db.String(255), nullable = False)
    id_user_payments = db.Column(db.Integer,db.ForeignKey("users.id"),nullable = False )
    # thêm kết nối:
    User_who_paid = db.relationship("Users", backref=db.backref("Events", lazy=True))
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime('%d-%m-%Y') if self.date else None,
            "total_bill": self.total_bill,
            "created_at": self.created_at.strftime('%H:%M:%S %Y-%m-%d') if self.created_at else None,
            "update_at": self.update_at.strftime('%H:%M:%S %Y-%m-%d') if self.update_at else None,
            "id_user_payments": self.id_user_payments,
            "tong_thu": self.tong_thu if self.tong_thu else 0,
            "tien_thua": self.tien_thua if self.tien_thua else 0,
            "status": self.status
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

class Event_User(db.Model):
    __tablename__ = "event_user"
    id = db.Column(db.Integer,primary_key= True)
    event_id = db.Column(db.Integer,db.ForeignKey("events.id"),nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)
    bonusthem = db.Column(db.String(255),nullable = False)
    bill_due = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(255), nullable = False )
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    id_user_payments = db.Column(db.Integer,nullable = True )
    
     # Thiết lập quan hệ với bảng Events và Users
    event = db.relationship("Events", backref=db.backref("event_users", lazy=True))
    user = db.relationship("Users", backref=db.backref("event_users", lazy=True))
    
    def to_dict(self):
        return{
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "bonusthem": self.bonusthem,
            "bill_due": self.bill_due,
            "status": self.status,
            "created_at": self.created_at.strftime('%H:%M:%S %Y-%m-%d'),
            "id_who_payments": self.id_user_payments
        }     
