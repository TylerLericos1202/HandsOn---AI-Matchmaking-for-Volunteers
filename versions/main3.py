import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-capstone-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///handson.db'

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- DATABASE MODELS ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    skills = db.Column(db.String(500), default="")  # e.g., "coding, tutoring"
    schedule = db.Column(db.String(500), default="") # e.g., "weekends"

# Create the database file automatically
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- TEMPLATES ---
NAV_BAR = """
<nav style="margin-bottom: 20px;">
    <a href="/">Home</a> | 
    {% if current_user.is_authenticated %}
        <span>Hi, {{ current_user.email }}</span> | <a href="/logout">Logout</a>
    {% else %}
        <a href="/login">Login</a> | <a href="/register">Register</a>
    {% endif %}
</nav>
<hr>
"""

# --- ROUTES ---
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        location = request.form.get("location")
        # --- THE AI MATCHMAKING SECRET SAUCE ---
        # If logged in, we inject their skills into the search query automatically!
        query = location
        if current_user.is_authenticated and current_user.skills:
            query = f"{location} volunteer {current_user.skills}"
        
        results = get_live_data(query)
        
    return render_template_string(f"{NAV_BAR} <h2>Search</h2> <form method='POST'><input name='location' placeholder='Location...'><button>Search</button></form> " + 
                                 "{% for r in results %}<div><a href='{{r.link}}'>{{r.title}}</a></div>{% endfor %}", 
                                 results=results)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(email=request.form['email'], password=hashed_pw, skills=request.form['skills'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(f"{NAV_BAR} <h2>Register</h2> <form method='POST'>Email: <input name='email'><br>Skills: <input name='skills' placeholder='e.g. teaching, tech'><br>Password: <input type='password' name='password'><br><button>Sign Up</button></form>")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template_string(f"{NAV_BAR} <h2>Login</h2> <form method='POST'>Email: <input name='email'><br>Password: <input type='password' name='password'><br><button>Login</button></form>")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def get_live_data(query):
    params = {"engine": "google", "q": query, "api_key": "YOUR_SERPAPI_KEY"}
    try:
        r = requests.get("https://serpapi.com/search", params=params)
        return r.json().get("organic_results", [])
    except: return []

if __name__ == "__main__":
    app.run(debug=True)