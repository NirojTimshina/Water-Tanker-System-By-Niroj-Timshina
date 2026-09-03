from flask import Blueprint, request, jsonify
from models import db, TankerRequest

request_bp = Blueprint('request_bp', __name__)


@request_bp.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    new_request = TankerRequest(
        household_id=data.get('household_id'),
        zone_id=data.get('zone_id'),
        urgency_level=data.get('urgency_level', 'normal'),
        status=data.get('status', 'pending'),
        quantity_needed=data.get('quantity_needed')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify(new_request.to_dict()), 201


@request_bp.route('/requests', methods=['GET'])
def get_requests():
    requests = TankerRequest.query.all()
    result = []
    for r in requests:
        result.append(r.to_dict())
    return jsonify(result), 200


@request_bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    req = TankerRequest.query.get(request_id)
    if req is None:
        error = dict()
        error['error'] = 'Request not found'
        return jsonify(error), 404
    return jsonify(req.to_dict()), 200


@request_bp.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    req = TankerRequest.query.get(request_id)
    if req is None:
        error = dict()
        error['error'] = 'Request not found'
        return jsonify(error), 404
    data = request.get_json()
    req.urgency_level = data.get('urgency_level', req.urgency_level)
    req.status = data.get('status', req.status)
    req.quantity_needed = data.get('quantity_needed', req.quantity_needed)
    db.session.commit()
    return jsonify(req.to_dict()), 200


@request_bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    req = TankerRequest.query.get(request_id)
    if req is None:
        error = dict()
        error['error'] = 'Request not found'
        return jsonify(error), 404
    db.session.delete(req)
    db.session.commit()
    message = dict()
    message['message'] = 'Request deleted successfully'
    return jsonify(message), 200