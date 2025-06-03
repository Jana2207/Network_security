import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os, sys
import numpy as np
import dill
import pickle

# Function to read a YAML file and return its content as a dictionary
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # Raise a custom exception in case of failure
        raise NetworkSecurityException(e, sys)
    
# Function to write content to a YAML file
# If replace=True, the existing file will be deleted before writing
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the existing file if it exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        with open(file_path, "w") as file:
            yaml.dump(content, file)  # Write content to YAML
    except Exception as e:
        # Raise a custom exception in case of failure
        raise NetworkSecurityException(e, sys)
