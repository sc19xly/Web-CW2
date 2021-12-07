from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                logging.error('Password Error')
                flash('Password is incorrect.', category='error')
        else:
            logging.error('Email Error')
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'), is_manager=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/change_password",methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_right = User.query.filter_by(email=email).first()
        username_right = User.query.filter_by(username=username).first()

        if not email_right:
            flash('Email is wrong.', category='error')
        elif not username_right:
            flash('Username is wrong.', category='error')
        elif check_password_hash(current_user.password, password1):
            flash('Please enter a different password!', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            current_user.password = generate_password_hash(password1, method='Sha256')
            db.session.add(current_user)
            db.session.commit()
            flash('Password Changed!')
            return redirect(url_for('auth.login'))
        return redirect(url_for("auth.change_password"))

    return render_template("change_password.html", user=current_user)


@auth.route("/new_manager", methods=['GET', 'POST'])
@login_required
def new_manager():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_manager:
                flash('The user is already a manager', category='error')
            else:
                if check_password_hash(user.password, password):
                    user.is_manager = True
                    db.session.add(user)
                    db.session.commit()
                    flash("Manager Added!", category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash('Password is incorrect.', category='error')
                    return redirect(url_for("auth.new_manager"))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for("auth.new_manager"))
        return redirect(url_for("auth.new_manager"))

    return render_template("new_manager.html", user=current_user)


@auth.route("/forget_password", methods=['POST', 'GET'])


def forget_password():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.username==username:
                if user.email==email:
                    return redirect(url_for("auth.change_password"))
                else:
                    flash('Email is incorrect.', category='error')
                    return redirect(url_for("auth.forget_password"))
            else:
                flash('Username is incorrect.', category='error')
                return redirect("auth.forget_password")
        else:
            flash('User does not exist.', category='error')
            return redirect(url_for("auth.forget_password"))
        return redirect(url_for("auth.forget_password"))

    return render_template("forget_password.html", user=current_user)
