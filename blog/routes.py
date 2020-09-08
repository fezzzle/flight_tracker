from flask import render_template, jsonify
from blog import app
from blog import search_from_db


class Observer:
    def __init__(self):
        self.flights = None
        self.geoJSON = None
    def on_data(self, flights, geoJSON):
        self.flights = flights
        self.geoJSON = geoJSON

data_source = Observer()
search_from_db.add_listener(data_source)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=data_source.flights, posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aviation')
@app.route('/aviation/')
def aviation():
    return render_template('aviation.html', flights=data_source.flights)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post's id is {post_id}"


@app.route('/user/<user>')
def show_user_profile(user):
    return render_template('user.html', user=user)


@app.route('/plane/<registration>')
def plane(registration):
    return render_template('plane.html', flights=data_source.flights, registration=registration)


@app.route('/aviation/api')
def get_flights():
    return jsonify(data_source.geoJSON)

@app.route('/aviation/map')
def get_map():
    return render_template('map.html', flights=data_source.flights)


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content about something cool',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content about something cool',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Timmyt Schafer',
        'title': 'Something about beer',
        'content': 'First post content about something cool',
        'date_posted': 'April 20, 2018'
    },
]
