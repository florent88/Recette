from datetime import datetime
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename #
import os #
from Recette import app , db 
from Recette.models import Recipe

UPLOAD_FOLDER = 'C:/Users/flore/OneDrive/Documents/save_stuff_here/Projet KIM/Recette/Recette/Recette/static/uploads/' #
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} #
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    recipes = Recipe.query.all()
    return render_template(
        'index.html',
        recipes = recipes,
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Recettes',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    """Displays the list of recipes and handles recipe creation."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        ingredients = request.form['ingredients']
        steps = request.form['steps'] #
        # Vérifiez si un fichier d'image a été téléchargé
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Vérifiez l'extension du fichier
                if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_file = filename
                else:
                    flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif)')
                    return redirect(request.url) #
        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, steps=steps, image_file=filename) #
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('recipes'))

    recipes = Recipe.query.all()
    return render_template(
        'recipes.html',
        title='Recettes',
        year=datetime.now().year,
        recipes=recipes
    )

@app.route('/recipes/<int:id>', methods=['GET', 'POST'])
def recipe(id):
    """Displays and handles updating a single recipe."""
    recipe = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.description = request.form.get('description', '')
        recipe.ingredients = request.form['ingredients']
        recipe.steps = request.form['steps']
        db.session.commit()
        return redirect(url_for('recipes'))

    return render_template(
        'recipe.html',
        title=recipe.title,
        year=datetime.now().year,
        recipe=recipe
    )

@app.route('/recipes/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    """Handles deleting a single recipe."""
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipes'))
