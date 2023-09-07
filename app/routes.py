import secrets
import os
import math
import json
from datetime import datetime
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image
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

start = [0]
passed = [0]
pack = [[]]
num = [0]

import tensorflow
import csv
from tensorflow.python.keras.models import load_model

tensorflow.keras.backend.clear_session()
model_best = load_model('best_model_101class.h5', compile=False)
# define label meaning
label = ['apple pie',
         'baby back ribs',
         'baklava',
         'beef carpaccio',
         'beef tartare',
         'beet salad',
         'beignets',
         'bibimbap',
         'bread pudding',
         'breakfast burrito',
         'bruschetta',
         'caesar salad',
         'cannoli',
         'caprese salad',
         'carrot cake',
         'ceviche',
         'cheese plate',
         'cheesecake',
         'chicken curry',
         'chicken quesadilla',
         'chicken wings',
         'chocolate cake',
         'chocolate mousse',
         'churros',
         'clam chowder',
         'club sandwich',
         'crab cakes',
         'creme brulee',
         'croque madame',
         'cup cakes',
         'deviled eggs',
         'donuts',
         'dumplings',
         'edamame',
         'eggs benedict',
         'escargots',
         'falafel',
         'filet mignon',
         'fish and_chips',
         'foie gras',
         'french fries',
         'french onion soup',
         'french toast',
         'fried calamari',
         'fried rice',
         'frozen yogurt',
         'garlic bread',
         'gnocchi',
         'greek salad',
         'grilled cheese sandwich',
         'grilled salmon',
         'guacamole',
         'gyoza',
         'hamburger',
         'hot and sour soup',
         'hot dog',
         'huevos rancheros',
         'hummus',
         'ice cream',
         'lasagna',
         'lobster bisque',
         'lobster roll sandwich',
         'macaroni and cheese',
         'macarons',
         'miso soup',
         'mussels',
         'nachos',
         'omelette',
         'onion rings',
         'oysters',
         'pad thai',
         'paella',
         'pancakes',
         'panna cotta',
         'peking duck',
         'pho',
         'pizza',
         'pork chop',
         'poutine',
         'prime rib',
         'pulled pork sandwich',
         'ramen',
         'ravioli',
         'red velvet cake',
         'risotto',
         'samosa',
         'sashimi',
         'scallops',
         'seaweed salad',
         'shrimp and grits',
         'spaghetti bolognese',
         'spaghetti carbonara',
         'spring rolls',
         'steak',
         'strawberry shortcake',
         'sushi',
         'tacos',
         'octopus balls',
         'tiramisu',
         'tuna tartare',
         'waffles'] # sorry
nu_link = 'https://www.nutritionix.com/food/'
nutrients = ['protein', 'fat', 'carbohydrates']

with open('nutrition101.csv', 'r') as file:
    reader = csv.reader(file)
    nutrition_table = dict()
    for i, row in enumerate(reader):
        if i == 0:
            name = ''
            continue
        else:
            name = row[1].strip()
        nutrition_table[name] = {
            'protein': float(row[2]),
            'fat': float(row[4]),
            'carbohydrates': float(row[5])
        }

@app.route('/history', methods=['GET', 'POST'])
def history():
    
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        qty = float(request.form['quantity'])
        info = json.loads(request.form['info'].replace('\'', '"'))
        for i in info:
            info[i] = f'{qty * float(info[i]) / 100:.2f}'
        submission = Submission(image_file=request.form['image'],
                                info=request.form['info'],
                                name=request.form['name'],
                                quantity=request.form['quantity'],
                                user_id=current_user.id)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('history'))
    submissions = Submission.query.filter_by(user_id=current_user.id).all()
    history = []
    for i in submissions:
        nutrients = json.loads(i.info.replace('\'', '"'))
        history.append({
            'name': i.name,
            'timestamp': datetime.timestamp(i.created_at),
            'image': i.image_file,
            'quantity': i.quantity,
            'protein': nutrients['protein'],
            'fat': nutrients['fat'],
            'carbohydrates': nutrients['carbohydrates'],
        })
    return render_template('history.html', history=history)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UploadForm()
    return render_template('submit.html', title='Submit', form=form)

@app.route('/upload', methods=['POST'])
def upload():
    tensorflow.keras.backend.clear_session()
    model_best = load_model('best_model_101class.h5', compile=False)
    file = request.files.getlist("img")
    for f in file:
        filename = secure_filename(str(num[0] + 500) + '.jpg')
        num[0] += 1
        name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('save name', name)
        f.save(name)
    pred_img = name
    pred_img = image.load_img(pred_img, target_size=(200, 200))
    pred_img = image.img_to_array(pred_img)
    pred_img = np.expand_dims(pred_img, axis=0)
    pred_img = pred_img / 255.

    pred = model_best.predict(pred_img)

    pa = dict()
    top = pred.argsort()[0][-3:]
    label.sort()
    _true = label[top[2]]
    # pa['image'] = f'{app.config["UPLOAD_FOLDER"]}/{i + 500}.jpg'
    pa['image'] = f'/uploads?filename={filename}'
    pa['result'] = _true
    pa['nutrition'] = nutrition_table[_true]
    pa['food'] = f'{nu_link}{_true}'
    pa['idx'] = i - start[0]
    pa['quantity'] = 100
    return render_template('results.html', p=pa)

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
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', title='Login', form=form)

@app.route('/uploads')
def uploads():
    return send_file(os.path.join('static\\uploads\\', request.args['filename']))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
