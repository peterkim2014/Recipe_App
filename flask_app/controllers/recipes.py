from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/homepage")
def homepage():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    user_id = session["user_id"]
    user = User.get_by_id(user_id)

    all_recipes = Recipe.get_all()
    # likes = Recipe.get_many_id(user_id)
    

    return render_template("home_page.html", all_recipes=all_recipes, user=user)

@app.route("/view/<int:id>")
def view_recipe(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    recipe = Recipe.get_many_id(id)
    user = User.get_by_id(session["user_id"])
    return render_template("view_recipe.html", recipe=recipe, user=user)