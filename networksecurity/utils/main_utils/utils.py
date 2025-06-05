import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os, sys
import numpy as np
import dill
import pickle

from sklearn.metrics import accuracy_score   
from sklearn.model_selection import GridSearchCV


# Function to read a YAML file and return its content as a dictionary
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # Raise a custom exception in case of failure
        raise NetworkSecurityException(e, sys) from e
    
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
        raise NetworkSecurityException(e, sys) from e
    
# Function to save data as numpy array
def save_data_of_numpy_array(file_path: str, array: np.array) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
# Function to save picke file
def save_object(file_path: str, obj: object) -> object:
    try:
        logging.info("Enters the save_object method of utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method from utils class")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

# Function to load object (pickle file)    
def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Function to load numpy array  
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Function to evaluate the models   
def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    """
    Evaluates multiple machine learning models using GridSearchCV to find the best hyperparameters.
    Returns a report of test accuracies and the best parameters of the last evaluated model.
    
    Parameters:
    - x_train, y_train: Training feature matrix and target vector
    - x_test, y_test: Test feature matrix and target vector
    - models: Dictionary of model names and their corresponding model instances
    - param: Dictionary of model names and their corresponding hyperparameter grids
    
    Returns:
    - report: Dictionary containing model names and their corresponding test accuracy
    - best_params: Dictionary of best hyperparameters from the last evaluated model
    """
    try:
        report = {}

        # Iterate over each model and its corresponding hyperparameter grid
        for i in range(len(models)):
            model = list(models.values())[i]  # Get model instance
            para = param[list(models.keys())[i]]  # Get corresponding parameter grid

            # Perform Grid Search Cross-Validation for hyperparameter tuning
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)

            # Set the best parameters obtained from GridSearch to the model
            model.set_params(**gs.best_params_)
            best_params = model.get_params()  # Store best parameters

            # Train the model with the best parameters
            model.fit(x_train, y_train)

            # Predict on training and testing datasets
            y_train_predict = model.predict(x_train)
            y_test_predict = model.predict(x_test)

            # Calculate accuracy scores
            train_model_score = accuracy_score(y_train, y_train_predict)
            test_model_score = accuracy_score(y_test, y_test_predict)

            # Store test accuracy in report dictionary with model name as key
            report[list(models.keys())[i]] = test_model_score

        return report, best_params

    except Exception as e:
        # Custom exception handling for better debugging/logging
        raise NetworkSecurityException(e, sys)
