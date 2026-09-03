from models.zone import db
from datetime import datetime

class TankerRequest(db.Model):
    __tablename__ = 'TANKERREQUESTS'

    request_id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer, db.ForeignKey('HOUSEHOLDS.household_id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('ZONES.zone_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    urgency_level = db.Column(db.String(20), default='normal')
    status = db.Column(db.String(20), default='pending')
    quantity_needed = db.Column(db.Integer)

    deliveries = db.relationship('DeliveryRecord', backref='request', lazy=True)

    def to_dict(self):
        result = dict()
        result['request_id'] = self.request_id
        result['household_id'] = self.household_id
        result['zone_id'] = self.zone_id
        result['urgency_level'] = self.urgency_level
        result['status'] = self.status
        result['quantity_needed'] = self.quantity_needed
        return result