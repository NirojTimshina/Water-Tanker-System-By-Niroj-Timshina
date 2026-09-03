from models.zone import db

class DeliveryRecord(db.Model):
    __tablename__ = 'DELIVERYRECORDS'

    delivery_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('TANKERREQUESTS.request_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('WATERSUPPLIERS.supplier_id'), nullable=False)
    delivery_date = db.Column(db.DateTime)
    delivery_time = db.Column(db.String(20))
    actual_quantity = db.Column(db.Integer)
    delay_hours = db.Column(db.Integer)
    payment_status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        result = dict()
        result['delivery_id'] = self.delivery_id
        result['request_id'] = self.request_id
        result['supplier_id'] = self.supplier_id
        result['delivery_date'] = self.delivery_date.isoformat() if self.delivery_date else None
        result['delivery_time'] = self.delivery_time
        result['actual_quantity'] = self.actual_quantity
        result['delay_hours'] = self.delay_hours
        result['payment_status'] = self.payment_status
        return result