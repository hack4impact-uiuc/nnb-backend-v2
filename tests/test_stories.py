import os
import unittest
from flask import jsonify
from api import app, db
from flask import Flask, request
from api.models import POI, Media, Link, Story, StoryPOI
import requests
from flask import jsonify
import json

poi1 = {
		  '_id' = 1
          'name': 'Himalayan Chimney',
          'date': 'Date(2018, 2, 27)',
          'description': 'Yum',
          'map_year': 2018,
          'x_coord': 12,
          'y_coord': 43
      }

poi2 = {
		  '_id' = 2
          'name': 'Mount Everest',
          'date': 'Date(2018, 5, 15)',
          'description': 'Snow',
          'map_year': 2018,
          'x_coord': 15,
          'y_coord': 30
      }

poi3 = {
		  '_id' = 3
          'name': 'Tampa Bay',
          'date': 'Date(2018, 8, 3)',
          'description': 'Hot',
          'map_year': 2018,
          'x_coord': 50,
          'y_coord': 82
      }

stories = [
			{
			  '_id': 21,
			  'story_name': 'Angad Goes to Wisconsin',
			},
			{
			  '_id': 22,
			  'story_name': 'Amanda Takes her Medicine',
			},
			{
			  '_id': 23,
			  'story_name': 'Jeffy Goes to Fashion Show',
			},
			{
			  '_id': 24,
			  'story_name': 'Time for Hack4Impact',
			}
		  ]
			
		  
story = {
			'_id': 25
			'story_name' : 'Jeffy Discovers the Dark side of the Moon'
		}

