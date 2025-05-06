from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db

# Modelo de base de datos para almacenar la información de la imagen subida
class ImageUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    image_path = db.Column(db.String(200))
    upload_time = db.Column(db.String(100))
    red_pixels = db.Column(db.Integer)
    green_pixels = db.Column(db.Integer)
    blue_pixels = db.Column(db.Integer)

