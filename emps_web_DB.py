from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static', static_url_path='')

# Database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'kodingtree.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===================== EMPLOYEE MODEL =======================
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)

    def json(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "job_role": self.job_role
        }

# ====================== STUDENT MODEL ========================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)

    def json(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "course": self.course,
            "mobile": self.mobile
        }

with app.app_context():
    db.create_all()

# ======================= STATIC PAGES ========================
@app.route('/')
def home():
    return app.send_static_file("index.html")

@app.route('/employees-page')
def emp_page():
    return app.send_static_file("employees.html")

@app.route('/students-page')
def std_page():
    return app.send_static_file("students.html")

# =============================================================
# EMPLOYEE CRUD API
# =============================================================

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    if not data:
        return {"error": "Invalid data"}, 400

    emp = Employee(
        emp_id=data['emp_id'],
        name=data['name'],
        job_role=data['job_role']
    )
    db.session.add(emp)
    db.session.commit()
    return emp.json(), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    all_emp = Employee.query.all()
    return jsonify([e.json() for e in all_emp])

# GET SINGLE EMPLOYEE
@app.route('/employees/<string:emp_id>', methods=['GET'])
def get_employee(emp_id):
    emp = Employee.query.filter_by(emp_id=emp_id).first()
    if not emp:
        abort(404)
    return emp.json()


@app.route('/employees/<string:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    emp = Employee.query.filter_by(emp_id=emp_id).first()
    if not emp:
        abort(404)

    data = request.get_json()
    emp.name = data.get("name", emp.name)
    emp.job_role = data.get("job_role", emp.job_role)
    db.session.commit()

    return emp.json()

@app.route('/employees/<string:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    emp = Employee.query.filter_by(emp_id=emp_id).first()
    if not emp:
        abort(404)

    db.session.delete(emp)
    db.session.commit()
    return "", 204

# =============================================================
# STUDENT CRUD API
# =============================================================

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    std = Student(
        student_id=data['student_id'],
        name=data['name'],
        course=data['course'],
        mobile=data['mobile'],
    )
    db.session.add(std)
    db.session.commit()
    return std.json(), 201


@app.route('/students', methods=['GET'])
def get_students():
    all_std = Student.query.all()
    return jsonify([s.json() for s in all_std])

# GET SINGLE STUDENT
@app.route('/students/<string:student_id>', methods=['GET'])
def get_student(student_id):
    std = Student.query.filter_by(student_id=student_id).first()
    if not std:
        abort(404)
    return std.json()


@app.route('/students/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    std = Student.query.filter_by(student_id=student_id).first()
    if not std:
        abort(404)

    data = request.get_json()
    std.name = data.get("name", std.name)
    std.course = data.get("course", std.course)
    std.mobile = data.get("mobile", std.mobile)
    db.session.commit()

    return std.json()


@app.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    std = Student.query.filter_by(student_id=student_id).first()
    if not std:
        abort(404)

    db.session.delete(std)
    db.session.commit()
    return "", 204


# =============================================================
if __name__ == '__main__':
    app.run(port=5000, debug=True)

