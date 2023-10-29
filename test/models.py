
## Define SQL Database tables

from datetime import datetime
from test import db

### Define user table
class User(db.Model):

    ## define column attributes
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean)
    
    ## one-to-many
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.is_admin}', '{self.email}', '{self.role}')"

    


### Define task table
class Task(db.Model):
    
    ## define column attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='To Do')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Task('{self.name}', '{self.status}', '{self.due_date}', '{self.user_id}')"

