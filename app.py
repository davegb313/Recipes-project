from flask import Flask
from flask import flash, render_template, request, url_for, session, redirect

from auth import Auth
from recipes import Recipes
import sqlite3

app = Flask(__name__)
app.secret_key = b'aj(>,m87hJn9+-alkjns*jkj90($'
DB_FILE_PATH = 'data/data.db'

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == ["GET"]:
        return render_template('login.html')

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    auth = Auth()
    if auth.login(username, password):
        return redirect('/recipes')

    flash('no-no')
    return render_template('login.html')


def isloggedin():
    if 'username' in session:
        return True


@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
#get the data from the front end
    if request.method == "GET":
        return render_template('sign-up.html')

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    password2 = request.form.get('password2', None)
    auth.create_user(username, password)
    auth.login(username, password) 
    return redirect('/recipes')


@app.route("/logout/")
def logout():
    auth = Auth()
    auth.logout()
    return redirect(url_for('show_recipes'))


@app.route("/")
@app.route("/recipes/")
def show_recipes():
    # If logged in, show recipes for the current user.
    # Otherwise, redirect to the Login page.
    auth = Auth()
        # get user id by the name
        # get all recipes
    if auth.is_logged_in():
        userid = auth.get_current_user()
        rec = Recipes()
        recipes = rec.get_recipes(userid)
        all_recipes = rec.get_all_recipes()
        return render_template('recipes.html', recipes=recipes, all_recipes=all_recipes)
    else:
        return redirect(url_for('login'))
    

@app.route("/recipes/new/", methods=['GET', 'POST'])
def add_recipe():
#     If request method is GET, load the 'add recipe' page.
    if request.method == "GET":
        return render_template('add_recipe.html')

#     If request method is POST:
#       1. Get all posted form data
#       2. Get ID of currently logged-in user
#       3. Call the relevant function of the Recipes class to add/create
#          a new record in the recipes table. Pass in the relevant 
#          information as arguments to the function.
#       4. Redirect to the Recipes (listing) page.

    title = request.form.get('recipe-title')
    image = request.form.get('recipe-image')
    category = request.form.get('recipe-category')
    description = request.form.get('recipe-description')
    ingredients = request.form.get('recipe-ingredients')
    
    auth = Auth()
    userid = auth.get_current_user()
    new_recipe = {
            'title': title,
            'image_URL': image,
            'category': category,
            'description': description,
            'ingredients': ingredients,
        }

    recipe = Recipes()
    recipe.add_recipe(new_recipe, userid)
    return redirect(url_for('show_recipes'))

 


@app.route("/recipes/<int:recipe_id>/")
def show_recipe(recipe_id):
    recipes = Recipes()
    recipe = recipes.get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)
    #Show the recipe that matches the given recipe ID

     



@app.route("/recipes/delete/<int:recipe_id>/")
def delete_recipe(recipe_id):
    auth = Auth()
    userid = auth.get_current_user()
    delete = Recipes()
    rec = delete.get_recipe(recipe_id)
    if rec['user_id'] == userid:
        delete.delete_recipe(recipe_id, userid)
        return redirect(url_for('show_recipes'))
    else:
        flash('This is not your recipe to delete')
        return redirect(url_for('show_recipe', recipe_id=recipe_id))