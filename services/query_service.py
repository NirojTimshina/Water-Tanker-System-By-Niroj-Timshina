from models import db, Zone, Household, WaterSupplier, TankerRequest, DeliveryRecord
from sqlalchemy import func


class QueryService:

    # SIMPLE QUERY 1: Get all households in a specific zone
    @staticmethod
    def get_households_by_zone(zone_id):
        households = Household.query.filter_by(zone_id=zone_id).all()
        result = []
        for h in households:
            result.append(h.to_dict())
        return result

    # SIMPLE QUERY 2: Get all tanker requests made by a specific household
    @staticmethod
    def get_requests_by_household(household_id):
        requests = TankerRequest.query.filter_by(household_id=household_id).all()
        result = []
        for r in requests:
            result.append(r.to_dict())
        return result

    # SIMPLE QUERY 3: Get all deliveries made by a specific supplier
    @staticmethod
    def get_deliveries_by_supplier(supplier_id):
        deliveries = DeliveryRecord.query.filter_by(supplier_id=supplier_id).all()
        result = []
        for d in deliveries:
            result.append(d.to_dict())
        return result

    # COMPLEX QUERY 1: Zone-wise water shortage severity
    # Joins Zones + TankerRequests + DeliveryRecords
    # Shows request count, emergency count, and average delay per zone
    @staticmethod
    def get_zone_shortage_report():
        results = db.session.query(
            Zone.zone_id,
            Zone.zone_name,
            func.count(TankerRequest.request_id).label('total_requests'),
            func.sum(
                db.case((TankerRequest.urgency_level == 'emergency', 1), else_=0)
            ).label('emergency_requests'),
            func.avg(DeliveryRecord.delay_hours).label('avg_delay_hours')
        ).join(
            TankerRequest, TankerRequest.zone_id == Zone.zone_id
        ).outerjoin(
            DeliveryRecord, DeliveryRecord.request_id == TankerRequest.request_id
        ).group_by(
            Zone.zone_id, Zone.zone_name
        ).all()

        report = []
        for row in results:
            entry = dict()
            entry['zone_id'] = row.zone_id
            entry['zone_name'] = row.zone_name
            entry['total_requests'] = row.total_requests
            entry['emergency_requests'] = int(row.emergency_requests) if row.emergency_requests else 0
            entry['avg_delay_hours'] = float(row.avg_delay_hours) if row.avg_delay_hours else 0
            report.append(entry)
        return report

    # COMPLEX QUERY 2: Supplier reliability report
    # Joins WaterSuppliers + DeliveryRecords + TankerRequests
    # Shows total deliveries, average delay, and total quantity delivered per supplier
    @staticmethod
    def get_supplier_reliability_report():
        results = db.session.query(
            WaterSupplier.supplier_id,
            WaterSupplier.supplier_name,
            func.count(DeliveryRecord.delivery_id).label('total_deliveries'),
            func.avg(DeliveryRecord.delay_hours).label('avg_delay_hours'),
            func.sum(DeliveryRecord.actual_quantity).label('total_quantity_delivered')
        ).join(
            DeliveryRecord, DeliveryRecord.supplier_id == WaterSupplier.supplier_id
        ).join(
            TankerRequest, TankerRequest.request_id == DeliveryRecord.request_id
        ).group_by(
            WaterSupplier.supplier_id, WaterSupplier.supplier_name
        ).all()

        report = []
        for row in results:
            entry = dict()
            entry['supplier_id'] = row.supplier_id
            entry['supplier_name'] = row.supplier_name
            entry['total_deliveries'] = row.total_deliveries
            entry['avg_delay_hours'] = float(row.avg_delay_hours) if row.avg_delay_hours else 0
            entry['total_quantity_delivered'] = int(row.total_quantity_delivered) if row.total_quantity_delivered else 0
            report.append(entry)
        return report