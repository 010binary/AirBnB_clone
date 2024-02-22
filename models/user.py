#!/usr/bin/python3
"""User Model"""
from .base_model import BaseModel


class User(BaseModel):
    """
    represents User
    email: (str)
    password: (str)
    first_name: (str)
    last_name: (str)
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""