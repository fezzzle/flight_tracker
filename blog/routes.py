from flask import render_template, jsonify
from blog import app
from blog import search_from_db
from blog import scrape_photos


class Observer:
    def __init__(self):
        self.flights = None
        self.flight_path = None
        self.geoJSON = None
        self.planes_not_in_db = None
        self.total_planes_in_db = None
    def on_data(self, flights, flight_path, geoJSON, planes_not_in_db, total_planes_in_db):
        self.flights = flights
        self.flight_path = flight_path
        self.geoJSON = geoJSON
        self.planes_not_in_db = planes_not_in_db
        self.total_planes_in_db = total_planes_in_db

data_source = Observer()
search_from_db.add_listener(data_source)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=data_source.flights, total_planes_in_db=data_source.total_planes_in_db)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/planes')
@app.route('/planes/')
def aviation():
    return render_template('planes.html', flights=data_source.flights, planes_not_in_db=data_source.planes_not_in_db)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post's id is {post_id}"


@app.route('/user/<user>')
def show_user_profile(user):
    return render_template('user.html', user=user)


@app.route('/plane/<registration>')
def plane(registration):
    image = scrape_photos.plane_img(registration)
    try:
        for plane in data_source.flights:
            if plane['registration'] == registration:
                flight = plane
        return render_template('plane.html', flight=flight, registration=registration, image=image)
    except Exception:
        print("This plane does not exist in our database!")
        return render_template(plane.html)



@app.route('/aviation/api')
def get_flights():
    return jsonify(data_source.geoJSON)


@app.route('/aviation/flight_data')
def flight_data():
    return jsonify(data_source.flight_path) 

@app.route('/aviation/map')
def get_map():
    return render_template('map.html', flights=data_source.flights)