#!/usr/bin/python3
"""Review Model"""
from .base_model import BaseModel


class Review(BaseModel):
    """
    represents Review
    Public class attributes:
        place_id: (str)
        user_id: (str)
        text: (str)
    """
    place_id = ""
    user_id = ""
    text = ""\n
