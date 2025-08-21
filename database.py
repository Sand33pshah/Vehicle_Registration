# database.py

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Vehicle model
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    licence_plate = db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    owner_name = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    make_model = db.Column(db.String(255), nullable=False)
    rto = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)
    emission_norm = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'licence_plate': self.licence_plate,
            'owner_name': self.owner_name,
            'registration_date': self.registration_date.isoformat(),
            'make_model': self.make_model,
            'rto': self.rto,
            'state': self.state,
            'fuel_type': self.fuel_type,
            'emission_norm': self.emission_norm,
            'vehicle_class': self.vehicle_class
        }