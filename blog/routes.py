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
    def on_data(self, flights, flight_path, geoJSON, planes_not_in_db):
        self.flights = flights
        self.flight_path = flight_path
        self.geoJSON = geoJSON
        self.planes_not_in_db = planes_not_in_db

data_source = Observer()
search_from_db.add_listener(data_source)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=data_source.flights, posts=posts)

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


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed rutrum faucibus orci ut convallis. Vestibulum ullamcorper nulla nec felis blandit, sit amet pellentesque sem dignissim. Duis pretium diam ex, sed sollicitudin justo bibendum in. Suspendisse bibendum vulputate eros a eleifend. Maecenas urna nisi, varius eu aliquet et, sagittis quis nisl. Suspendisse aliquet neque non turpis ultrices, ac sagittis massa maximus. In molestie ut diam aliquam auctor. Sed vitae bibendum lectus. Etiam facilisis accumsan pharetra. Integer sagittis dolor eu mollis condimentum. Vestibulum tempor tempor sapien vel vestibulum. Nam a sapien ac metus dignissim sollicitudin ac at libero. Duis vitae porttitor risus. Donec euismod dapibus cursus. Praesent sed volutpat tortor, id condimentum ante. In eget facilisis ex.',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Phasellus quam neque, cursus vel lorem dictum, elementum tristique arcu. Fusce placerat orci a enim sagittis, eget tristique elit sagittis. Nulla sit amet tortor sed ex aliquam aliquam. Proin purus neque, pretium nec porta faucibus, iaculis cursus justo. Nullam nec risus vel nisi pellentesque gravida. Sed malesuada commodo quam, et dignissim lacus. Proin vestibulum blandit velit et eleifend. Mauris augue orci, volutpat sed lectus id, posuere semper dolor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nunc scelerisque tempus ligula nec placerat. Nullam a dui sed tellus lacinia tempor. Ut ac risus ac augue sodales pulvinar in vehicula risus.',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Phasellus quam neque, cursus vel lorem dictum, elementum tristique arcu. Fusce placerat orci a enim sagittis, eget tristique elit sagittis. Nulla sit amet tortor sed ex aliquam aliquam. Proin purus neque, pretium nec porta faucibus, iaculis cursus justo. Nullam nec risus vel nisi pellentesque gravida. Sed malesuada commodo quam, et dignissim lacus. Proin vestibulum blandit velit et eleifend. Mauris augue orci, volutpat sed lectus id, posuere semper dolor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nunc scelerisque tempus ligula nec placerat. Nullam a dui sed tellus lacinia tempor. Ut ac risus ac augue sodales pulvinar in vehicula risus.',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'Phasellus quam neque, cursus vel lorem dictum, elementum tristique arcu. Fusce placerat orci a enim sagittis, eget tristique elit sagittis. Nulla sit amet tortor sed ex aliquam aliquam. Proin purus neque, pretium nec porta faucibus, iaculis cursus justo. Nullam nec risus vel nisi pellentesque gravida. Sed malesuada commodo quam, et dignissim lacus. Proin vestibulum blandit velit et eleifend. Mauris augue orci, volutpat sed lectus id, posuere semper dolor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nunc scelerisque tempus ligula nec placerat. Nullam a dui sed tellus lacinia tempor. Ut ac risus ac augue sodales pulvinar in vehicula risus.',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Timmyt Schafer',
        'title': 'Something about beer',
        'content': 'Phasellus quam neque, cursus vel lorem dictum, elementum tristique arcu. Fusce placerat orci a enim sagittis, eget tristique elit sagittis. Nulla sit amet tortor sed ex aliquam aliquam. Proin purus neque, pretium nec porta faucibus, iaculis cursus justo. Nullam nec risus vel nisi pellentesque gravida. Sed malesuada commodo quam, et dignissim lacus. Proin vestibulum blandit velit et eleifend. Mauris augue orci, volutpat sed lectus id, posuere semper dolor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nunc scelerisque tempus ligula nec placerat. Nullam a dui sed tellus lacinia tempor. Ut ac risus ac augue sodales pulvinar in vehicula risus.',
        'date_posted': 'April 20, 2018'
    },
]
