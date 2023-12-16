# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phrases.db'
db = SQLAlchemy(app)

app.template_folder = 'templates'
app.static_folder = 'static'

class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    phrases = Phrase.query.order_by(Phrase.id.desc()).limit(1).all()
    return render_template('index.html', phrases=phrases)

@app.route('/ajouter_phrase', methods=['POST'])
def ajouter_phrase():
    nouvelle_phrase = request.form['phrase']
    nouvelle_phrase_obj = Phrase(text=nouvelle_phrase)
    db.session.add(nouvelle_phrase_obj)
    db.session.commit()
    return index()

if __name__ == '__main__':
    with app.app_context():  # Ajout du contexte d'application Flask
        db.create_all()
    app.run(debug=True)
