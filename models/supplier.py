from models.zone import db

class WaterSupplier(db.Model):
    __tablename__ = 'WATERSUPPLIERS'

    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    tanker_capacity_liters = db.Column(db.Integer)
    price_per_tanker = db.Column(db.Numeric(10, 2))

    # Relationship: One supplier has many delivery records
    deliveries = db.relationship('DeliveryRecord', backref='supplier', lazy=True)

    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'phone': self.phone,
            'tanker_capacity_liters': self.tanker_capacity_liters,
            'price_per_tanker': float(self.price_per_tanker) if self.price_per_tanker else None
        }