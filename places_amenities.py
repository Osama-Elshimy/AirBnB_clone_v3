#!/usr/bin/python3
"""Places amenities view module"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, abort, jsonify
