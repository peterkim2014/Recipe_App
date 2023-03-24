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

@app.route("/recipes/new")
def create_recipe_page():
    return render_template("add_recipe.html")

@app.route("/recipes/new/create", methods=["POST"])
def create_recipe_form():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "duration": request.form["duration"],
        "user_id": session["user_id"]
    }
    if Recipe.validate_recipe(data):
        Recipe.save(data)
        return redirect("/homepage")
    else:
        return redirect("/homepage")

@app.route("/edit/<int:id>")
def edit_recipe_page(id):
    recipe = Recipe.get_by_id(id)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/edit/recipe", methods=["POST"])
def edit_recipe():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    recipe = Recipe.get_by_id(request.form["id"])
    if not recipe or recipe.user_id != session["user_id"]:
        return redirect("/homepage")
    
@app.route("/delete/<int:id>")
def delete_recipe(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    Recipe.delete(id)
    return redirect("/homepage")