from flask import Blueprint, request, jsonify
from models import db, WaterSupplier

supplier_bp = Blueprint('supplier_bp', __name__)


@supplier_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = WaterSupplier(
        supplier_name=data.get('supplier_name'),
        phone=data.get('phone'),
        tanker_capacity_liters=data.get('tanker_capacity_liters'),
        price_per_tanker=data.get('price_per_tanker')
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify(new_supplier.to_dict()), 201


@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = WaterSupplier.query.all()
    result = []
    for s in suppliers:
        result.append(s.to_dict())
    return jsonify(result), 200


@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = WaterSupplier.query.get(supplier_id)
    if supplier is None:
        error = dict()
        error['error'] = 'Supplier not found'
        return jsonify(error), 404
    return jsonify(supplier.to_dict()), 200


@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = WaterSupplier.query.get(supplier_id)
    if supplier is None:
        error = dict()
        error['error'] = 'Supplier not found'
        return jsonify(error), 404
    data = request.get_json()
    supplier.supplier_name = data.get('supplier_name', supplier.supplier_name)
    supplier.phone = data.get('phone', supplier.phone)
    supplier.tanker_capacity_liters = data.get('tanker_capacity_liters', supplier.tanker_capacity_liters)
    supplier.price_per_tanker = data.get('price_per_tanker', supplier.price_per_tanker)
    db.session.commit()
    return jsonify(supplier.to_dict()), 200


@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = WaterSupplier.query.get(supplier_id)
    if supplier is None:
        error = dict()
        error['error'] = 'Supplier not found'
        return jsonify(error), 404
    db.session.delete(supplier)
    db.session.commit()
    message = dict()
    message['message'] = 'Supplier deleted successfully'
    return jsonify(message), 200