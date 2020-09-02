from flask import render_template, jsonify
from blog import app
from blog import search_from_db


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=search_from_db.flights, posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aviation')
@app.route('/aviation/')
def aviation():
    return render_template('aviation.html', flights=search_from_db.flights)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post's id is {post_id}"


@app.route('/user/<user>')
def show_user_profile(user):
    return render_template('user.html', user=user)


@app.route('/plane/<registration>')
def plane(registration):
    return render_template('plane.html', flights=search_from_db.flights, registration=registration)


@app.route('/aviation/api')
def get_flights():
    return jsonify(search_from_db.geoJSON)

@app.route('/aviation/map')
def get_map():
    return render_template('map.html', flights=search_from_db.flights)


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
