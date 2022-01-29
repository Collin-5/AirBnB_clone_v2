#!/usr/bin/python3
"""
Defines engine DBStorage
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from sqlalchemy.orm import sessionmaker
from models.state import State
from models.city import City
from models import classes


class DBStorage:
    """
    Create SQLAlchemy database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
            Create engine and link to MySQL databse (hbnb_dev, hbnb_dev_db)
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env_var = ("HBNB_ENV", "none")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.
                                      format(user, pwd, db),
                                      pool_pre_ping=True)
        if env_var == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves dictionary of objects in database
        Args:
            cls (obj): class of objects to be queried
        Returns:
            dictionary of objects
        """
        objs_dict = {}
        objs = [v for k, v in classes.items()]
        if cls:
            if isinstance(cls, str):
                cls = classes[cls]
            objs = [cls]
        for c in objs:
            for instance in self.__session.query(c):
                key = str(instance.__class__.__name__) + "." + str(instance.id)
                objs_dict[key] = instance
        return (objs_dict)

    def new(self, obj):
        """
        Adds the object to the current db session
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from current database session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        commits alll changes
        """
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """
        closes a session
        """
        self.__session.close()
