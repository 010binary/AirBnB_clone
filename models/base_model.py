#!/usr/bin/python3
"""
A BaseModel class that defines all common attributes/methods for other classes.
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """
    Class initialization.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialing...
        Created_at, id, Updated_at and the time_format instance.
        Created_at, Updated_at are set to the isoformat using the
        .isoformat method.
        """
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if "created_at" == key:
                    self.created_at = datetime.strptime(kwargs["created_at"],
                                                        date_format)
                elif "updated_at" == key:
                    self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                        date_format)
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        private instance method.
        Prints the string representation of
        [<class name>] (<self.id>) <self.__dict__>
        """
        return ('[{}] ({}) {}'.
                format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """
        updates the public instance attribute updated_at with
        the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dict_obj containing all keys/values
        of __dict__ of the instance.
        """
        dic = self.__dict__.copy()
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()
        dic["__class__"] = self.__class__.__name__
        return dic

    def __repr__(self) -> str:
        """
        returns string representation
        Returns:
            str: _Object_
        """
        return (self.__str__())\n
