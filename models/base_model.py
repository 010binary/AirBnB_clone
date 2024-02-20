#!/usr/bin/python3
"""
A BaseModel class that defines all common attributes/methods for other classes.
"""

from datetime import datetime
import uuid

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
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)
            

    def __str__(self):
        """
        private instance method.
        Prints the string representation of
        [<class name>] (<self.id>) <self.__dict__>
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute updated_at with
        the current datetime.
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
        
    def to_dict(self):
        """
        returns a dict_obj containing all keys/values
        of __dict__ of the instance.
        """
        dict_obj = {}
        dict_obj.update(self.__dict__)
        dict_obj.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dict_obj['created_at'] = self.created_at.isoformat()
        dict_obj['updated_at'] = self.updated_at.isoformat()
        return dict_obj
