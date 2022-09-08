from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db 
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email= email).first() #check if user email exists in database

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category= 'success')
                login_user(user, remember= True)
                return redirect('/')
            else:
                flash("Incorrect Password, try again", category= 'error')
        else:
            flash("Email Already Exists")


    return render_template('login.html', user= current_user)

@auth.route('/logout')
@login_required #will make sure that an user is logged in otherwise can't see "logout" 
def logout():
    logout_user() #logs out the current user
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods= ['GET', 'POST'])
def sign_up():
    #get form post items
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #validation
        user = User.query.filter_by(email= email).first()
        if user: #check if user email exists in database
            flash('Email ID already exists')
        elif len(email) < 4:
            flash('Email Must Be Greater Than 3 Characters', category= 'error')
        elif len(first_name) < 2:
            flash('First Name Must Be Greater Than 1 Characters', category= 'error')
        elif password1 != password2:
            flash('Passwords does not match', category= 'error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category= 'error')
        else:
            #create new user account/Add to user database
            new_user = User(email= email, first_name= first_name, password= generate_password_hash(password1, method= "sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember= True)
            flash('Account created successfully', category= 'success')
            return redirect('/')


    return render_template('sign_up.html', user= current_user)