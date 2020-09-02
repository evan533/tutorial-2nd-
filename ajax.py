import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'app.db')
db = SQLAlchemy(app)

# database #
class Human(db.Model):
    height = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)

# routing #
@app.route('/')
def home():
    return render_template('abcd.html')

@app.route('/tutorial', methods=['GET','POST'])
def tutorial():
    print(len(Human.query.all()))
    data = Human.query.all()
    return render_template('tutorial.html')

@app.route('/sendData', methods=['GET', 'POST'])
def sendData():
    height = None
    name = None
    gender = None
    if request.method == 'POST':
        height = request.form['height']
        name = request.form['name']
        gender = request.form['gender']
        user = Human(height = height, name = name, gender = gender)
        db.session.add(user)
        db.session.commit()

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    data = Human.query.all()
    human = []
    for person in data:
       human.append({
           'height': person.height,
           'name': person.name,
           'gender': person.gender
       })
    return jsonify(human)
