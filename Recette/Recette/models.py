from Recette import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


