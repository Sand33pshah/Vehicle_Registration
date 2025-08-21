# app.py (updated)

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from database import db, Vehicle  # Import from your new file

# Create a Flask app instance
app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with the app
db.init_app(app)

# API key for a simple, private access control
API_KEY = "your_secret_api_key_here"

# Create the database and table on the first run
with app.app_context():
    db.create_all()

# --- API Endpoints ---

# Frontend landing page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to add new vehicle data
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()

    required_fields = ['licence_plate', 'owner_name', 'registration_date', 'make_model', 'rto', 'state', 'fuel_type', 'emission_norm', 'vehicle_class']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing or empty field: {field}'}), 400

    if Vehicle.query.get(data['licence_plate']):
        return jsonify({'error': 'Licence plate already exists.'}), 409

    try:
        new_vehicle = Vehicle(
            licence_plate=data['licence_plate'],
            owner_name=data['owner_name'],
            registration_date=datetime.strptime(data['registration_date'], '%Y-%m-%d').date(),
            make_model=data['make_model'],
            rto=data['rto'],
            state=data['state'],
            fuel_type=data['fuel_type'],
            emission_norm=data['emission_norm'],
            vehicle_class=data['vehicle_class']
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve vehicle data
@app.route('/api/vehicles/<string:licence_plate>', methods=['GET'])
def get_vehicle(licence_plate):
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Unauthorized access. Invalid API Key.'}), 401

    vehicle = Vehicle.query.get(licence_plate)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found.'}), 404

    return jsonify(vehicle.to_dict()), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)