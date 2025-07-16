import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'cyberlab_secret')

# Database config
DB_USER = os.environ.get('DB_USER', 'cyberlab_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'cyberlab_pwd')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'cyberlab')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    documents = db.relationship('Document', backref='owner', lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_metadata():
    metadata_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'metadata.json')
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template('home.html', metadata=metadata)

@app.route('/login', methods=['GET', 'POST'])
def login():
    metadata = load_metadata()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('lab'))
        flash('Invalid credentials', 'error')
    return render_template('login.html', metadata=metadata)

@app.route('/register', methods=['GET', 'POST'])
def register():
    metadata = load_metadata()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', metadata=metadata)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/lab', methods=['GET', 'POST'])
@login_required
def lab():
    metadata = load_metadata()
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            doc = Document(user_id=current_user.id, filename=filename, filepath=filepath)
            db.session.add(doc)
            db.session.commit()
            flash('Document uploaded successfully.', 'success')
        else:
            flash('Only PDF files are allowed.', 'error')
    documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template('lab.html', metadata=metadata, documents=documents)

@app.route('/download/<int:file_id>')
@login_required
def download(file_id):
    # Vulnérabilité IDOR : pas de vérification d'appartenance
    doc = Document.query.filter_by(id=file_id).first()
    if not doc or not os.path.exists(doc.filepath):
        abort(404)
    return send_file(doc.filepath, as_attachment=True, download_name=doc.filename)

@app.route('/api/metadata')
def api_metadata():
    return json.dumps(load_metadata())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 