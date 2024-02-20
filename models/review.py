#!/usr/bin/python3
"""Review Model"""
from .base_model import BaseModel


class Review(BaseModel):
    """represents Review"""
    place_id = ""
    user_id = ""
    text = ""
