import secrets
import os
from flask import render_template, url_for, flash, redirect, request, send_file
from app import app, db, bcrypt
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Submission
from app.forms import RegistrationForm, LoginForm, UploadForm

@app.route('/')
def index():
    print(current_user.is_authenticated)
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, pass_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.pass_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/uploads')
def uploads():
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], request.args['filename']))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['photo']
        filename = secrets.token_urlsafe(16)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(url_for('uploads', filename=filename))
    else:
        print('error', form.errors)
    return render_template('submit.html', title='Submit', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
