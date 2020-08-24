from flask import render_template
from blog import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', flights=flights, posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aviation')
def aviation():
    return render_template('aviation.html', flights=flights)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post's id is {post_id}"


@app.route('/user/<user>')
def show_user_profile(user):
    return render_template('user.html', user=user)


flights = [
    {
        "airline": "Lufthansa",
        "aircraft": "Airbus A380",
        "registration": "D-AIMA",
        "flown_est": 5,
        "visit_eetn": False,
        "speed": "453kt",
        "destination": "EDDF",
        "alt": 35000
    },
    {
        "airline": "British Airways",
        "aircraft": "Boeing 777",
        "registration": "G-STBE",
        "flown_est": 21,
        "visit_eetn": False,
        "speed": "460kt",
        "destination": "EGLL",
        "alt": 35000
    }
]


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
