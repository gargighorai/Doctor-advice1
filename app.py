from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from fpdf import FPDF

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
# ---------------------
# Database Models
# ---------------------
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    diagnosis = db.Column(db.String(200))

# ---------------------
# Routes
# ---------------------
@app.route('/')
def home():
    if 'doctor' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        doctor = Doctor.query.filter_by(username=request.form['username']).first()
        if doctor and check_password_hash(doctor.password, request.form['password']):
            session['doctor'] = doctor.username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('doctor', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'doctor' not in session:
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients, doctor_name=session['doctor'])

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = Patient(
            name=request.form['name'],
            age=request.form['age'],
            diagnosis=request.form['diagnosis']
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_patient.html')

@app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.diagnosis = request.form['diagnosis']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_patient.html', patient=patient)


# ---------------------
# Init command
# ---------------------
@app.cli.command('init-db')
def init_db():
    db.create_all()
    if not Doctor.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123')
        admin = Doctor(username='admin', password=hashed_pw)
        db.session.add(admin)
        db.session.commit()
    print('Database initialized and admin created.')

# ---------------------
# Run app
# ---------------------
import os
from init_db import init_database
init_database(app, db, Doctor)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

