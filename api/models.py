from api import db
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

class Poi(db.Model):
    """PointOfInterest"""
    __tablename__ = "poi"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=False)
    map_year = db.Column(db.Integer, nullable=False)
    x_coord = db.Column(db.Float, nullable=False)
    y_coord = db.Column(db.Float, nullable=False)

    #One-to-many relationships
    media = db.relationship('Media', backref='poi', lazy=True)
    links = db.relationship('Link', backref='poi', lazy=True)
    story_pois = db.relationship('Story_Poi', backref='poi', lazy=True)

class Media(db.Model):
    """Media"""
    __tablename__ = "media"

    id = db.Column(db.Integer, unique=True, primary_key=True) 
    content_url = db.Column(db.String, nullable=True)
    caption = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='SET NULL'), nullable=True)

class Link(db.Model):
    """Link"""
    __tablename__ = "link"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    link_url = db.Column(db.String, nullable=True)
    display_name = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='SET NULL'), nullable=True)

class Story(db.Model):
    """Story"""
    __tablename__ = "story"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    story_name = db.Column(db.String, nullable=False)

    #One-to-many relationship
    story_poi = db.relationship('Story_Poi', backref='story')

class Story_Poi(db.Model):
    """Story_Poi"""
    __tablename__ = "story_poi"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='SET NULL'), nullable=True)


# class Person(db.Model):
#     """Person"""
#     __tablename__ = "person"

#     id = db.Column(db.Integer, unique=True, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     emails = db.relationship('Email',backref='emails')

#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return '<name {}>'.format(self.name)

# class Email(db.Model):
#     """Email"""
#     __tablename__ = "email"
    
#     id = db.Column(db.Integer, unique=True, primary_key=True)
#     email = db.Column(db.String, nullable=False)
#     person = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='SET NULL'), nullable=True)

#     def __init__(self, email):
#             self.email = email

#     def __repr__(self):
#         return '<email {}>'.format(self.email)