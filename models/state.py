#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")

    else:
        name = ""

    @property
    def cities(self):
        """
        getter attribute
        returns a list of City instances
        """
        lcities = []
        for city in models.storage.all("City").values():
            if city.state_id == self.id:
                lcities.append(city)
        return lcities
