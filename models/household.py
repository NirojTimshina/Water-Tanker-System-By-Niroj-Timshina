from models.zone import db

class Household(db.Model):
    __tablename__ = 'HOUSEHOLDS'

    household_id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('ZONES.zone_id'), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    family_size = db.Column(db.Integer)

    requests = db.relationship('TankerRequest', backref='household', lazy=True)

    def to_dict(self):
        result = dict()
        result['household_id'] = self.household_id
        result['zone_id'] = self.zone_id
        result['owner_name'] = self.owner_name
        result['phone'] = self.phone
        result['address'] = self.address
        result['family_size'] = self.family_size
        return result