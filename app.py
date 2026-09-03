from flask import Flask, jsonify
from models import db, Zone, Household, WaterSupplier, TankerRequest, DeliveryRecord
from routes.zone_routes import zone_bp
from routes.household_routes import household_bp
from routes.supplier_routes import supplier_bp
from routes.request_routes import request_bp
from routes.delivery_routes import delivery_bp
from routes.query_routes import query_bp
from routes.page_routes import page_bp
from background_tasks.scheduler import start_scheduler
import oracledb

app = Flask(__name__)
app.secret_key = "water_tanker_secret_key_2026"

DB_USER = "water_tanker_user"
DB_PASSWORD = "Water123"
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "XEPDB1"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(zone_bp)
app.register_blueprint(household_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(request_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(query_bp)
app.register_blueprint(page_bp)


if __name__ == '__main__':
    with app.app_context():
        start_scheduler(app, db, TankerRequest)
    app.run(debug=True, use_reloader=False)