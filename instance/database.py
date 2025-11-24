# database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# On crée l'objet db, mais on ne lui donne pas encore l'application Flask.
db = SQLAlchemy()


class Member(db.Model):
    __tablename__ = "members"  # nom de la table dans association.db

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)  # Prénom
    last_name = db.Column(db.String(100), nullable=False)   # Nom
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Cotisation payée ? (True/False)
    dues = db.Column(db.Boolean, default=False)

    # Statut du membre : "Actif", "Inactif", etc.
    status = db.Column(db.String(30), default="Actif")

    # Date d’inscription
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    # Date/heure de l’événement
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
