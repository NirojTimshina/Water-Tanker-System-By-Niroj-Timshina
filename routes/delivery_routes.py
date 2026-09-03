from flask import Blueprint, request, jsonify
from models import db, DeliveryRecord

delivery_bp = Blueprint('delivery_bp', __name__)


@delivery_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    data = request.get_json()
    new_delivery = DeliveryRecord(
        request_id=data.get('request_id'),
        supplier_id=data.get('supplier_id'),
        delivery_time=data.get('delivery_time'),
        actual_quantity=data.get('actual_quantity'),
        delay_hours=data.get('delay_hours'),
        payment_status=data.get('payment_status', 'pending')
    )
    db.session.add(new_delivery)
    db.session.commit()
    return jsonify(new_delivery.to_dict()), 201


@delivery_bp.route('/deliveries', methods=['GET'])
def get_deliveries():
    deliveries = DeliveryRecord.query.all()
    result = []
    for d in deliveries:
        result.append(d.to_dict())
    return jsonify(result), 200


@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    delivery = DeliveryRecord.query.get(delivery_id)
    if delivery is None:
        error = dict()
        error['error'] = 'Delivery not found'
        return jsonify(error), 404
    return jsonify(delivery.to_dict()), 200


@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    delivery = DeliveryRecord.query.get(delivery_id)
    if delivery is None:
        error = dict()
        error['error'] = 'Delivery not found'
        return jsonify(error), 404
    data = request.get_json()
    delivery.delivery_time = data.get('delivery_time', delivery.delivery_time)
    delivery.actual_quantity = data.get('actual_quantity', delivery.actual_quantity)
    delivery.delay_hours = data.get('delay_hours', delivery.delay_hours)
    delivery.payment_status = data.get('payment_status', delivery.payment_status)
    db.session.commit()
    return jsonify(delivery.to_dict()), 200


@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    delivery = DeliveryRecord.query.get(delivery_id)
    if delivery is None:
        error = dict()
        error['error'] = 'Delivery not found'
        return jsonify(error), 404
    db.session.delete(delivery)
    db.session.commit()
    message = dict()
    message['message'] = 'Delivery deleted successfully'
    return jsonify(message), 200