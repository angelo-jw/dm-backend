
from app import db


class PaymentTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    carrier = db.Column(db.String(64))
    door_knock_commission = db.Column(db.Boolean)
