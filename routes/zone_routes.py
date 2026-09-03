from flask import Blueprint, request, jsonify
from models import db, Zone

zone_bp = Blueprint('zone_bp', __name__)

@zone_bp.route('/zones', methods=['POST'])
def create_zone():
    data = request.get_json()
    new_zone = Zone(
        zone_name=data.get('zone_name'),
        ward_number=data.get('ward_number'),
        population_estimate=data.get('population_estimate')
    )
    db.session.add(new_zone)
    db.session.commit()
    return jsonify(new_zone.to_dict()), 201

@zone_bp.route('/zones', methods=['GET'])
def get_zones():
    zones = Zone.query.all()
    result = []
    for zone in zones:
        result.append(zone.to_dict())
    return jsonify(result), 200

@zone_bp.route('/zones/<int:zone_id>', methods=['GET'])
def get_zone(zone_id):
    zone = Zone.query.get(zone_id)
    if zone is None:
        return jsonify({"error": "Zone not found"}), 404
    return jsonify(zone.to_dict()), 200

@zone_bp.route('/zones/<int:zone_id>', methods=['PUT'])
def update_zone(zone_id):
    zone = Zone.query.get(zone_id)
    if zone is None:
        return jsonify({"error": "Zone not found"}), 404
    data = request.get_json()
    zone.zone_name = data.get('zone_name', zone.zone_name)
    zone.ward_number = data.get('ward_number', zone.ward_number)
    zone.population_estimate = data.get('population_estimate', zone.population_estimate)
    db.session.commit()
    return jsonify(zone.to_dict()), 200

@zone_bp.route('/zones/<int:zone_id>', methods=['DELETE'])
def delete_zone(zone_id):
    zone = Zone.query.get(zone_id)
    if zone is None:
        return jsonify({"error": "Zone not found"}), 404
    db.session.delete(zone)
    db.session.commit()
    return jsonify({"message": "Zone deleted successfully"}), 200