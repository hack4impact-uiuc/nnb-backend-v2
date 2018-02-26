from api import db
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

#TODO: implement toDict functions

class POI(db.Model):
    """Point of interest table"""
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
    story_pois = db.relationship('StoryPOI', backref='poi', lazy=True)

    def __repr__(self):
        return '<name {}>'.format(self.name)

class Media(db.Model):
    """Media table"""
    __tablename__ = "media"

    id = db.Column(db.Integer, unique=True, primary_key=True) 
    content_url = db.Column(db.String, nullable=True)
    caption = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<content_url {}>'.format(self.content_url)

class Link(db.Model):
    """Link table"""
    __tablename__ = "link"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    link_url = db.Column(db.String, nullable=True)
    display_name = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<additional_links poi_id = {}>'.format(self.poi_id)

class Map(db.Model):
    """Map table"""
    __tablename__ = "map"

    id = db.Column(db.Integer, unique=True, primary_key=True) 
    image_url = db.Column(db.String, nullable=False)
    map_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<map {}>'.format(self.map_year)

class Story(db.Model):
    """Story table"""
    __tablename__ = "story"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    story_name = db.Column(db.String, nullable=False)

    #One-to-many relationship
    story_pois = db.relationship('StoryPOI', backref='story')

    def __repr__(self):
        return '<story_names {}>'.format(self.story_name)

class StoryPOI(db.Model):
    """Story POIs table"""
    __tablename__ = "story_poi"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id", ondelete='CASCADE'), nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<stories {}>'.format(self.id)
