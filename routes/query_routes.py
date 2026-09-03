from flask import Blueprint, jsonify
from services.query_service import QueryService

query_bp = Blueprint('query_bp', __name__)


# SIMPLE QUERY 1: Households in a zone
@query_bp.route('/zones/<int:zone_id>/households', methods=['GET'])
def households_by_zone(zone_id):
    result = QueryService.get_households_by_zone(zone_id)
    return jsonify(result), 200


# SIMPLE QUERY 2: Requests by a household
@query_bp.route('/households/<int:household_id>/requests', methods=['GET'])
def requests_by_household(household_id):
    result = QueryService.get_requests_by_household(household_id)
    return jsonify(result), 200


# SIMPLE QUERY 3: Deliveries by a supplier
@query_bp.route('/suppliers/<int:supplier_id>/deliveries', methods=['GET'])
def deliveries_by_supplier(supplier_id):
    result = QueryService.get_deliveries_by_supplier(supplier_id)
    return jsonify(result), 200


# COMPLEX QUERY 1: Zone-wise shortage report
@query_bp.route('/reports/zone-shortage', methods=['GET'])
def zone_shortage_report():
    result = QueryService.get_zone_shortage_report()
    return jsonify(result), 200


# COMPLEX QUERY 2: Supplier reliability report
@query_bp.route('/reports/supplier-reliability', methods=['GET'])
def supplier_reliability_report():
    result = QueryService.get_supplier_reliability_report()
    return jsonify(result), 200