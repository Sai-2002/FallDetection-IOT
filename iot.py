from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sweswe'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot_users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable=False)
    n_name = db.Column(db.String(80), nullable=False)
    n_no = db.Column(db.String(20), nullable=False)
    g_name = db.Column(db.String(80), nullable=False)
    g_no = db.Column(db.String(20), nullable=False)
    h_type = db.Column(db.String(80), nullable=False)
    h_name = db.Column(db.String(80), nullable=False)
    h_no = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float,  nullable=False)
    weight = db.Column(db.Float,  nullable=False)
    gender = db.Column(db.String(10),  nullable=False)


@app.route('/')
def index():
    return "Welcome to the user registration and login system."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        phone_no = data['phone_no']
        name = data['name']
        g_name = data['g_name']
        g_no = data['g_no']
        n_name = data['n_name']
        n_no = data['n_no']
        h_type = data['h_type']
        h_name = data['h_name']
        password = data['password']
        h_no = data['password']
        age = data['age']
        weight = data['weight']
        height = data['height']
        gender = data['gender']
        existing_user = User.query.filter_by(phone_no=phone_no).first()
        if existing_user:
            return "invalid"
            #flash('Account already exists. Please choose a different one.')
        else:
            new_user = User(phone_no=phone_no, password=generate_password_hash(password, method='sha256'), name = name, g_name=g_name, n_name = n_name,
                            g_no=g_no, n_no=n_no,h_type = h_type, h_name=h_name, h_no = h_no, age = age, weight = weight, height = height,gender = gender)
            db.session.add(new_user)
            db.session.commit()
            #flash('Registration successful. You can now log in.')
            return redirect(url_for('login'))
    
    return "registering"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        phone_no = data['phone_no']
        password = data['password']

        user = User.query.filter_by(phone_no=phone_no).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful.')
            return "login success"
        else:
            return "login failed"
            #flash('Login failed. Please check your username and password.')

    return "login"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def reverse_geocode(lat, lng, api_key):
    # Google Maps Geocoding API endpoint
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    # Parameters for the request
    params = {
        "latlng": f"{lat},{lng}",
        "key": api_key,
    }

    # Send a GET request to the API
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK" and data['results']:
            # Extract the formatted address from the results
            formatted_address = data['results'][0]['formatted_address']
            return formatted_address
        else:
            return "Location not found"
    else:
        return "Error in the API request"
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        model = "model name podu"
        data = request.get_json()
        gyro_x = data['gyro_x']
        gyro_y = data['gyro_y']
        gyro_z = data['gyro_z']
        longitude = data['long']
        latitude = data['latt']
        pulse = data['pulse']
        acc_x = data['acc_x']
        acc_y = data['acc_y']
        acc_z = data['acc_z']



        input_data = np.array([[gyro_x, gyro_y, gyro_z, pulse, acc_x,acc_y,acc_z]])
        
        prediction = model.predict(input_data)

        response = {'prediction': prediction[0]}
        api_key = "your_api_key"
        location = reverse_geocode(latitude, longitude, api_key)

        print(location)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8082)



# Replace 'your_api_key' with your actual Google Maps Geocoding API key
