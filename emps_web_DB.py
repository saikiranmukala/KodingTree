from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

# Serve static website
app = Flask(__name__, static_folder='static', static_url_path='')

# ---- DATABASE CONFIG ----
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(DB_DIR, 'employees.db')

# create instance folder if not exists
os.makedirs(DB_DIR, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---- MODEL ----
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "emp_id": self.emp_id,
            "name": self.name,
            "job_role": self.job_role
        }


# Create DB tables
with app.app_context():
    db.create_all()


# ---- STATIC WEBSITE ROOT ----
@app.route('/')
def index():
    return app.send_static_file('index.html')


# ---- API ROUTES ----

# Create Employee
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()

    if not data or 'emp_id' not in data or 'name' not in data or 'job_role' not in data:
        return jsonify({"error": "emp_id, name, and job_role are required"}), 400

    if Employee.query.filter_by(emp_id=data['emp_id']).first():
        return jsonify({"error": "Employee ID already exists"}), 400

    emp = Employee(
        emp_id=data['emp_id'],
        name=data['name'],
        job_role=data['job_role']
    )

    db.session.add(emp)
    db.session.commit()

    return jsonify(emp.to_json()), 201


# Get All Employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.to_json() for e in employees])


# Get Employee by emp_id
@app.route('/employees/<string:emp_id>', methods=['GET'])
def get_employee(emp_id):
    emp = Employee.query.filter_by(emp_id=emp_id).first()
    if not emp:
        abort(404)
    return jsonify(emp.to_json())


# Update Employee
@app.route('/employees/<string:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()
    emp = Employee.query.filter_by(emp_id=emp_id).first()

    if not emp:
        abort(404)

    if 'name' in data:
        emp.name = data['name']
    if 'job_role' in data:
        emp.job_role = data['job_role']

    db.session.commit()
    return jsonify(emp.to_json())


# Delete Employee
@app.route('/employees/<string:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    emp = Employee.query.filter_by(emp_id=emp_id).first()

    if not emp:
        abort(404)

    db.session.delete(emp)
    db.session.commit()

    return '', 204


# ---- RUN APP ----
if __name__ == '__main__':
    app.run(port=6000, debug=True)
