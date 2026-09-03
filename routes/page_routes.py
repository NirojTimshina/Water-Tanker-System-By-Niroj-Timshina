from flask import Blueprint, render_template, request, redirect, session
from models import db, Zone, Household, WaterSupplier, TankerRequest, DeliveryRecord
from services.query_service import QueryService

page_bp = Blueprint('page_bp', __name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ---------- LOGIN / LOGOUT ----------
@page_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@page_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')


# ---------- DASHBOARD ----------
@page_bp.route('/')
@login_required
def dashboard():
    return render_template('index.html')


# ---------- ZONES ----------
@page_bp.route('/zones-page')
@login_required
def zones_page():
    zones = Zone.query.all()
    return render_template('zones.html', zones=zones)


@page_bp.route('/zones-page/add', methods=['POST'])
@login_required
def add_zone_page():
    new_zone = Zone(
        zone_name=request.form.get('zone_name'),
        ward_number=request.form.get('ward_number') or None,
        population_estimate=request.form.get('population_estimate') or None
    )
    db.session.add(new_zone)
    db.session.commit()
    return redirect('/zones-page')


@page_bp.route('/zones-page/delete/<int:zone_id>', methods=['POST'])
@login_required
def delete_zone_page(zone_id):
    zone = Zone.query.get(zone_id)
    if zone:
        db.session.delete(zone)
        db.session.commit()
    return redirect('/zones-page')


# ---------- HOUSEHOLDS ----------
@page_bp.route('/households-page')
@login_required
def households_page():
    households = Household.query.all()
    return render_template('households.html', households=households)


@page_bp.route('/households-page/add', methods=['POST'])
@login_required
def add_household_page():
    new_household = Household(
        zone_id=request.form.get('zone_id'),
        owner_name=request.form.get('owner_name'),
        phone=request.form.get('phone'),
        address=request.form.get('address'),
        family_size=request.form.get('family_size') or None
    )
    db.session.add(new_household)
    db.session.commit()
    return redirect('/households-page')


@page_bp.route('/households-page/delete/<int:household_id>', methods=['POST'])
@login_required
def delete_household_page(household_id):
    household = Household.query.get(household_id)
    if household:
        db.session.delete(household)
        db.session.commit()
    return redirect('/households-page')


# ---------- SUPPLIERS ----------
@page_bp.route('/suppliers-page')
@login_required
def suppliers_page():
    suppliers = WaterSupplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)


@page_bp.route('/suppliers-page/add', methods=['POST'])
@login_required
def add_supplier_page():
    new_supplier = WaterSupplier(
        supplier_name=request.form.get('supplier_name'),
        phone=request.form.get('phone'),
        tanker_capacity_liters=request.form.get('tanker_capacity_liters') or None,
        price_per_tanker=request.form.get('price_per_tanker') or None
    )
    db.session.add(new_supplier)
    db.session.commit()
    return redirect('/suppliers-page')


@page_bp.route('/suppliers-page/delete/<int:supplier_id>', methods=['POST'])
@login_required
def delete_supplier_page(supplier_id):
    supplier = WaterSupplier.query.get(supplier_id)
    if supplier:
        db.session.delete(supplier)
        db.session.commit()
    return redirect('/suppliers-page')


# ---------- REQUESTS ----------
@page_bp.route('/requests-page')
@login_required
def requests_page():
    requests = TankerRequest.query.all()
    return render_template('requests.html', requests=requests)


@page_bp.route('/requests-page/add', methods=['POST'])
@login_required
def add_request_page():
    new_request = TankerRequest(
        household_id=request.form.get('household_id'),
        zone_id=request.form.get('zone_id'),
        urgency_level=request.form.get('urgency_level'),
        quantity_needed=request.form.get('quantity_needed') or None
    )
    db.session.add(new_request)
    db.session.commit()
    return redirect('/requests-page')


@page_bp.route('/requests-page/update-status/<int:request_id>', methods=['POST'])
@login_required
def update_request_status(request_id):
    req = TankerRequest.query.get(request_id)
    if req:
        req.status = request.form.get('status')
        db.session.commit()
    return redirect('/requests-page')


@page_bp.route('/requests-page/delete/<int:request_id>', methods=['POST'])
@login_required
def delete_request_page(request_id):
    req = TankerRequest.query.get(request_id)
    if req:
        db.session.delete(req)
        db.session.commit()
    return redirect('/requests-page')


# ---------- DELIVERIES ----------
@page_bp.route('/deliveries-page')
@login_required
def deliveries_page():
    deliveries = DeliveryRecord.query.all()
    return render_template('deliveries.html', deliveries=deliveries)


@page_bp.route('/deliveries-page/add', methods=['POST'])
@login_required
def add_delivery_page():
    new_delivery = DeliveryRecord(
        request_id=request.form.get('request_id'),
        supplier_id=request.form.get('supplier_id'),
        delivery_time=request.form.get('delivery_time'),
        actual_quantity=request.form.get('actual_quantity') or None,
        delay_hours=request.form.get('delay_hours') or None
    )
    db.session.add(new_delivery)
    db.session.commit()
    return redirect('/deliveries-page')


@page_bp.route('/deliveries-page/update-status/<int:delivery_id>', methods=['POST'])
@login_required
def update_delivery_status(delivery_id):
    delivery = DeliveryRecord.query.get(delivery_id)
    if delivery:
        delivery.payment_status = request.form.get('payment_status')
        db.session.commit()
    return redirect('/deliveries-page')


@page_bp.route('/deliveries-page/delete/<int:delivery_id>', methods=['POST'])
@login_required
def delete_delivery_page(delivery_id):
    delivery = DeliveryRecord.query.get(delivery_id)
    if delivery:
        db.session.delete(delivery)
        db.session.commit()
    return redirect('/deliveries-page')


# ---------- REPORTS ----------
@page_bp.route('/reports-page')
@login_required
def reports_page():
    zone_report = QueryService.get_zone_shortage_report()
    supplier_report = QueryService.get_supplier_reliability_report()
    return render_template('reports.html', zone_report=zone_report, supplier_report=supplier_report)