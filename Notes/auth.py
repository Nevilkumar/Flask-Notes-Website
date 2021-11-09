from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_required, current_user, logout_user, login_user

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET','POST'])
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email = email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash('Logged in Successfully!!!', category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect Password, Try Again.', category='danger')
            else:
                flash('Email Doesn\'t Exists.', category='danger')
        return render_template('login.html')
        

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/signup/', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password1 = request.form.get('password')
            password2 = request.form.get('confirm-password')

            user = User.query.filter_by(email = email).first()
            if user:
                flash('Email Already Exists.', category='danger')
            elif password1!=password2:
                flash('Passwords Dont\'t Match.', category='danger')
            else:
                new_user = User(email=email,username=username,password=generate_password_hash(password1,method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created Successfully!!!', category='success')
                return redirect(url_for('views.home'))
        return render_template('signup.html')
    
