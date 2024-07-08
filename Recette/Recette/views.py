from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from Recette import app, db 
from Recette.models import Recipe
from Recette.models import User


UPLOAD_FOLDER = 'C:/Users/flore/OneDrive/Documents/save_stuff_here/Projet KIM/Recette/Recette/Recette/static/uploads/' #
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} #
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
@login_required
def recipes():
    """Displays the list of recipes and handles recipe creation."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        ingredients = request.form['ingredients']
        steps = request.form['steps'] #
        # Vérifiez si un fichier d'image a été téléchargé
        filename = None

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Vérifiez l'extension du fichier
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif)')
                    return redirect(request.url)
        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, steps=steps, image_file=filename, user_id = current_user.id) #
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
@login_required
def recipe(id):
    """Displays and handles updating a single recipe."""
    recipe = Recipe.query.filter_by(user_id=current_user.id).all()

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Check if the user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')