"""Custom exception class for the project"""
from enum import Enum

class Error(Exception,Enum):
    no_response = 1