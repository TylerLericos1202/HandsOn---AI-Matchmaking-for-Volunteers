import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'handson-capstone-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///handson.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELS ---
class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    skills = db.Column(db.String(500), default="")
    availability = db.Column(db.String(500), default="") 
    saved_items = db.relationship('SavedOpportunity', backref='user', lazy=True)

class SavedOpportunity(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    link = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

MY_KEY = "your key here"

# --- ROUTES ---

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        location = request.form.get("location")
        query = f"{location} volunteer"
        if current_user.is_authenticated:
            if current_user.skills:
                query += f" {current_user.skills}"
            if current_user.availability:
                query += f" {current_user.availability}"
        
        params = {"engine": "google", "q": query, "api_key": MY_KEY}
        try:
            r = requests.get("https://serpapi.com/search", params=params)
            results = r.json().get("organic_results", [])
        except: pass
    return render_template("index.html", results=results)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(
            email=request.form['email'], 
            password=hashed_pw, 
            skills=request.form.get('skills', ''),
            availability=request.form.get('availability', '') 
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login')) # This will work now!
    return render_template("auth.html", title="Register")

# ADDED THIS: The missing login function
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template("auth.html", title="Login")

# ADDED THIS: The missing save function
@app.route("/save", methods=["POST"])
@login_required
def save_opportunity():
    title = request.form.get("title")
    link = request.form.get("link")
    exists = SavedOpportunity.query.filter_by(link=link, user_id=current_user.id).first()
    if not exists:
        new_save = SavedOpportunity(title=title, link=link, user_id=current_user.id)
        db.session.add(new_save)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route("/delete_save/<int:save_id>", methods=["POST"])
@login_required
def delete_save(save_id):
    item = SavedOpportunity.query.get_or_404(save_id)
    # Security check: Make sure the user owns this item
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.skills = request.form.get("skills")
        current_user.availability = request.form.get("availability")
        db.session.commit()
        return redirect(url_for('profile'))
    saved = SavedOpportunity.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", saved=saved)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
