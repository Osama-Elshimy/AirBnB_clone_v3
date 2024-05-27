#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage_type


class State(BaseModel, Base):
    """State class"""

    if storage_type == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            from models.__init__ import storage
            from models.city import City

            return [
                city
                for city in storage.all(City).values()
                if city.state_id == self.id
            ]
