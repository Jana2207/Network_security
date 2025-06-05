# Standard imports
import os
import sys
import pandas as pd
import numpy as np

# Project-specific logging and exception handling
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

# Entities for configuration and artifacts
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainingArtifact
)
from networksecurity.entity.config_entity import ModelTrainingConfig

# Utilities and helpers
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metrics.classification_report import get_classification_score
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models
)

# ML models and metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)

# MLflow for model tracking
import mlflow

class ModelTrainer:
    """
    Handles the training of multiple classification models, evaluates their performance,
    tracks metrics using MLflow, and saves the best model.
    """
    
    def __init__(self,
                 model_training_config: ModelTrainingConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_config = model_training_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_model(self, best_model, trainining_classification_metrics, testing_classification_metrics):
        """
        Logs model performance metrics and model object to MLflow.
        """
        with mlflow.start_run():
            # Extract training and testing metrics
            training_accuracy = trainining_classification_metrics.accuracy
            testing_accuracy = testing_classification_metrics.accuracy
            training_precision = trainining_classification_metrics.precision_score
            testing_precision = testing_classification_metrics.precision_score
            training_recall = trainining_classification_metrics.recall
            testing_recall = testing_classification_metrics.recall
            training_f1_score = trainining_classification_metrics.f1_score
            testing_f1_score = testing_classification_metrics.f1_score
            training_auc_roc = trainining_classification_metrics.auc_roc
            testing_auc_roc = testing_classification_metrics.auc_roc

            # Log metrics to MLflow
            mlflow.log_metrics({
                "training_accuracy": training_accuracy,
                "testing_accuracy": testing_accuracy,
                "training_precision": training_precision,
                "testing_precision": testing_precision,
                "training_recall": training_recall,
                "testing_recall": testing_recall,
                "training_f1_score": training_f1_score,
                "testing_f1_score": testing_f1_score,
                "training_auc_roc": training_auc_roc,
                "testing_auc_roc": testing_auc_roc
            })

            # Log the model object itself
            mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, x_train, y_train, x_test, y_test):
        """
        Trains multiple models, selects the best based on accuracy, tracks performance,
        and saves the final model object.
        """

        # Define candidate models
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        # Define hyperparameters for each model
        params = {
            "Decision Tree": {
            'criterion': ['gini', 'entropy', 'log_loss'],
            # 'splitter': ['best', 'random'],
            # 'max_features': ['sqrt', 'log2'],
            },
            "Random Forest": {
            'criterion': ['gini', 'entropy', 'log_loss'],
            # 'max_features': ['sqrt', 'log2', None],
            # 'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Gradient Boosting": {
            'loss': ['log_loss', 'exponential'],
            # 'learning_rate': [0.1, 0.01, 0.05, 0.001],
            # 'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
            # 'criterion': ['squared_error', 'friedman_mse'],
            # 'max_features': ['auto', 'sqrt', 'log2'],
            # 'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {
            'penalty': ['l1', 'l2', 'elasticnet', 'none'],
            # 'C': [0.01, 0.1, 1, 10],
            # 'solver': ['newton-cg', 'lbfgs', 'liblinear', 'saga'],
            # 'max_iter': [100, 200, 500],
            },
            "AdaBoost": {
            'learning_rate': [0.1, 0.01, 0.001],
            # 'n_estimators': [8, 16, 32, 64, 128, 256],
            }
        }


        # Evaluate all models with GridSearchCV
        model_report, best_params = evaluate_models(
            x_train=x_train,
            x_test=x_test,
            y_train=y_train,
            y_test=y_test,
            models=models,
            param=params
        )

        # Get the best model based on test score
        best_model_score = max(model_report.values())
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        # Predict on both train and test sets using the best model
        y_train_predict = best_model.predict(x_train)
        y_test_predict = best_model.predict(x_test)

        logging.info(f"Best model: {best_model} with parameters: {best_params} and score: {best_model_score}")
        print(f"Best model: {best_model} with parameters: {best_params} and score: {best_model_score}")

        # Get classification metrics for train and test
        classification_train_metrics = get_classification_score(
            y_true=y_train,
            y_pred=y_train_predict,
            print_report=True
        )
        classification_test_metrics = get_classification_score(
            y_true=y_test,
            y_pred=y_test_predict,
            print_report=True
        )

        logging.info(f"Train metrics: {classification_train_metrics}")
        print(f"Train metrics: {classification_train_metrics}")
        logging.info(f"Test metrics: {classification_test_metrics}")
        print(f"Test metrics: {classification_test_metrics}")

        # Track model and metrics using MLflow
        self.track_model(
            best_model=best_model,
            trainining_classification_metrics=classification_train_metrics,
            testing_classification_metrics=classification_test_metrics
        )

        # Load preprocessing object used during transformation
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

        # Create model directory if it doesn’t exist
        model_dir_path = os.path.dirname(self.model_training_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        # Combine preprocessor and model into a single pipeline object
        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

        # Save the final pipeline and raw model
        save_object(self.model_training_config.trained_model_file_path, obj=Network_model)
        save_object("final_model/model.pkl", best_model)

        # Create and return artifact
        model_traininig_artifact = ModelTrainingArtifact(
            trained_model_path=self.model_training_config.trained_model_file_path,
            train_metric_artifact=classification_train_metrics,
            test_metric_artifact=classification_test_metrics
        )

        logging.info(f"Model trainer artifact: {model_traininig_artifact}")
        return model_traininig_artifact

    def initiate_model_training(self) -> ModelTrainingArtifact:
        """
        Loads transformed data and initiates the model training process.
        """
        try:
            # Load train and test numpy arrays
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            # Split arrays into features and labels
            X_train, Y_train, X_test, Y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # Train and return the model training artifact
            model_training_artifact = self.train_model(X_train, Y_train, X_test, Y_test)
            return model_training_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
