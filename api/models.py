from api import db
from api.utils import Mixin
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy

class User(Mixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    salt = db.Column(db.String, nullable=False)
    pw_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<username {} >'.format(self.username)

class POI(Mixin, db.Model):
    __tablename__ = 'poi'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=False)
    map_year = db.Column(db.Integer, nullable=False)
    x_coord = db.Column(db.Float, nullable=False)
    y_coord = db.Column(db.Float, nullable=False)

    #One-to-many relationships
    media = db.relationship('Media', cascade="all, delete-orphan")
    links = db.relationship('Link', cascade="all, delete-orphan")
    story_pois = db.relationship('StoryPOI', cascade="all, delete-orphan")

    def __repr__(self):
        return '<name {}>'.format(self.name)

class Media(Mixin, db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, unique=True, primary_key=True) 
    content_url = db.Column(db.String, nullable=True)
    caption = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<content_url {}>'.format(self.content_url)

class Link(Mixin, db.Model):
    __tablename__ = 'link'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    link_url = db.Column(db.String, nullable=True)
    display_name = db.Column(db.String, nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<additional_links poi_id = {}>'.format(self.poi_id)

class Map(Mixin, db.Model):
    __tablename__ = 'map'

    id = db.Column(db.Integer, unique=True, primary_key=True) 
    image_url = db.Column(db.String, nullable=False)
    map_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<map {}>'.format(self.map_year)

class Story(Mixin, db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    story_name = db.Column(db.String, nullable=False)

    #One-to-many relationship
    story_pois = db.relationship('StoryPOI', cascade="all, delete-orphan")

    def __repr__(self):
        return '<story_names {}>'.format(self.story_name)

class StoryPOI(Mixin, db.Model):
    __tablename__ = 'story_poi'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id', ondelete='CASCADE'), nullable=True)
    poi_id = db.Column(db.Integer, db.ForeignKey('poi.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return '<stories {}>'.format(self.id)
