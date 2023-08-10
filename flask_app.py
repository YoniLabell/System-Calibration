from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calibration.db'
db = SQLAlchemy(app)

class Systems(db.Model):
    system_id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(100), nullable=False)
    system_type = db.Column(db.String(50), nullable=False)
    calibration_tests = db.relationship('CalibrationTests', secondary='system_calibration_tests', backref='systems')

    @staticmethod
    def create_system(system_name, system_type):
        new_system = Systems(system_name=system_name, system_type=system_type)
        db.session.add(new_system)
        db.session.commit()

    @staticmethod
    def get_all_systems():
        return Systems.query.all()

    @staticmethod
    def get_system_by_id(system_id):
        return Systems.query.get(system_id)

    @staticmethod
    def update_system(system, new_name, new_type):
        system.system_name = new_name
        system.system_type = new_type
        db.session.commit()

    @staticmethod
    def delete_system(system):
        db.session.delete(system)
        db.session.commit()

class CalibrationTests(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)


class SystemCalibrationTests(db.Model):
    system_calibration_tests_id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.system_id'))
    test_id = db.Column(db.Integer, db.ForeignKey('calibration_tests.test_id'))
    last_calibration_date = db.Column(db.DateTime, nullable=True)
    test_interval = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET'])
def index():
    systems= Systems.get_all_systems()
    return render_template('index.html',systems=systems)

@app.route('/add_system', methods=['POST','GET'])
def add_system():
    if request.method == 'GET':
        return render_template('add_systems.html')
    else:
        system_name = request.form.get('system_name')
        system_type = request.form.get('system_type')
        Systems.create_system(system_name, system_type)
        return redirect(url_for('index'))

@app.route('/edit_system/<int:system_id>', methods=['GET', 'POST'])
def edit_system(system_id):
    system = Systems.get_system_by_id(system_id)
    if request.method == 'POST':
        new_name = request.form.get('new_name')
        new_type = request.form.get('new_type')
        Systems.update_system(system, new_name, new_type)
        return redirect(url_for('index'))
    return render_template('edit_system.html', system=system)

@app.route('/delete_system/<int:system_id>')
def delete_system(system_id):
    system = Systems.get_system_by_id(system_id)
    Systems.delete_system(system)
    return redirect(url_for('index'))

