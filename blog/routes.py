from flask import render_template, jsonify
from blog import app
import asyncio
from blog import search_from_db

loop = asyncio.get_event_loop()
flights = loop.run_until_complete(search_from_db.main())
print(flights)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=flights, posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aviation')
@app.route('/aviation/')
def aviation():
    return render_template('aviation.html', flights=flights)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post's id is {post_id}"


@app.route('/user/<user>')
def show_user_profile(user):
    return render_template('user.html', user=user)


@app.route('/plane/<registration>')
def plane(registration):
    return render_template('plane.html', flights=flights, registration=registration)


@app.route('/aviation/flights_api')
def get_flights():
    return jsonify(flights)

@app.route('/aviation/map')
def get_map():
    return render_template('map.html', flights=flights)


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
