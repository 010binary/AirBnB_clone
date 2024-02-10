#!/usr/bin/python3
"""User Model"""
import BaseModel

class User(BaseModel):
    """Represents a user
    Attrebutes:
        email: string - empty string
        password: string - empty string
        first_name: string - empty string
        last_name: string - empty string
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self):
        """Initializer"""
        super().__init__()
