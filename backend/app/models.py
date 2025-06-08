from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    rating = db.Column(db.Float)


class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_msg = db.Column(db.String(300))
    bot_reply = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
