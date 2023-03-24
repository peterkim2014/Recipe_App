from flask import render_template, flash, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("login_page.html")

@app.route("/user/register", methods=["POST"])
def create_user_form():
    
    if User.validate_registration(request.form):
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        User.create(data)
        flash("Thank you for registering", "registration")
        return redirect("/")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login_page_form():

    user = User.get_by_email(request.form["email"])

    if user == None or bcrypt.check_password_hash(user.password, request.form["password"]) == False:
        flash("Invalid Credentials", "login")
        return redirect("/")

    session["user_id"] = user.id
    print(session["user_id"])
    flash("Login Successful")
    return redirect("/homepage")