from flask import Blueprint, request, jsonify
from models import db, Household

household_bp = Blueprint('household_bp', __name__)


@household_bp.route('/households', methods=['POST'])
def create_household():
    data = request.get_json()
    new_household = Household(
        zone_id=data.get('zone_id'),
        owner_name=data.get('owner_name'),
        phone=data.get('phone'),
        address=data.get('address'),
        family_size=data.get('family_size')
    )
    db.session.add(new_household)
    db.session.commit()
    return jsonify(new_household.to_dict()), 201


@household_bp.route('/households', methods=['GET'])
def get_households():
    households = Household.query.all()
    result = []
    for h in households:
        result.append(h.to_dict())
    return jsonify(result), 200


@household_bp.route('/households/<int:household_id>', methods=['GET'])
def get_household(household_id):
    household = Household.query.get(household_id)
    if household is None:
        error = dict()
        error['error'] = 'Household not found'
        return jsonify(error), 404
    return jsonify(household.to_dict()), 200


@household_bp.route('/households/<int:household_id>', methods=['PUT'])
def update_household(household_id):
    household = Household.query.get(household_id)
    if household is None:
        error = dict()
        error['error'] = 'Household not found'
        return jsonify(error), 404
    data = request.get_json()
    household.owner_name = data.get('owner_name', household.owner_name)
    household.phone = data.get('phone', household.phone)
    household.address = data.get('address', household.address)
    household.family_size = data.get('family_size', household.family_size)
    db.session.commit()
    return jsonify(household.to_dict()), 200


@household_bp.route('/households/<int:household_id>', methods=['DELETE'])
def delete_household(household_id):
    household = Household.query.get(household_id)
    if household is None:
        error = dict()
        error['error'] = 'Household not found'
        return jsonify(error), 404
    db.session.delete(household)
    db.session.commit()
    message = dict()
    message['message'] = 'Household deleted successfully'
    return jsonify(message), 200