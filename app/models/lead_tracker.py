from app import db


class LeadTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lead_date = db.Column(db.DateTime)
    lead_vendor = db.Column(db.String(64))
    lead_spend = db.Column(db.Float)
    lead_quantity = db.Column(db.Integer)
