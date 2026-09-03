from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Zone(db.Model):
    __tablename__ = 'ZONES'

    zone_id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(100), nullable=False)
    ward_number = db.Column(db.Integer)
    population_estimate = db.Column(db.Integer)

    # Relationship: One zone has many households
    households = db.relationship('Household', backref='zone', lazy=True)
    # Relationship: One zone has many tanker requests
    requests = db.relationship('TankerRequest', backref='zone', lazy=True)

    def to_dict(self):
        return {
            'zone_id': self.zone_id,
            'zone_name': self.zone_name,
            'ward_number': self.ward_number,
            'population_estimate': self.population_estimate
        }