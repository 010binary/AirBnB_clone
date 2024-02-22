#!/usr/bin/python3
"""State Model"""
from .base_model import BaseModel


class City(BaseModel):
    """
    represents City
    state_id: (str) 
    name: (str)
    """
    state_id = ""
    name = ""