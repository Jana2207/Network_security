import os
import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.constant.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMETERS
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact
)

from networksecurity.utils.main_utils.utils import (
    save_data_of_numpy_array,
    save_object
)

class DataTransformation:
    """
    Handles data preprocessing tasks such as missing value imputation,
    transformation, and preparation for modeling.
    """

    def __init__(self,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        Initialize with paths and config required for data transformation.
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads a CSV file and returns it as a DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @classmethod
    def get_data_transformation_object(cls) -> Pipeline:
        """
        Initializes and returns a Pipeline with KNN imputation.
        """
        logging.info("Entered get_data_transformation_object method of DataTransformation class")
        try:
            # Create KNNImputer with parameters defined in constants
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMETERS)
            logging.info(f"Initializing KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMETERS}")
            # Create pipeline with imputer step
            processor = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Executes the full data transformation process and returns an artifact.
        """
        logging.info("Entered into the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting the data transformation")

            # Load training and testing data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Separate features and target for training data
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            # Separate features and target for testing data
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # Initialize preprocessing pipeline and fit on training data
            processor = self.get_data_transformation_object()
            pre_processor_obj = processor.fit(input_feature_train_df)

            # Transform both training and testing feature sets
            transformed_input_train_feature = pre_processor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = pre_processor_obj.transform(input_feature_test_df)

            # Concatenate features and target column back into final arrays
            train_array = np.concatenate((transformed_input_train_feature,
                                          target_feature_train_df.values.reshape(-1, 1)), axis=1)
            test_array = np.concatenate((transformed_input_test_feature,
                                         target_feature_test_df.values.reshape(-1, 1)), axis=1)

            # Save transformed arrays as .npy files
            save_data_of_numpy_array(self.data_transformation_config.tranformed_train_file_path,
                                     array=train_array)
            save_data_of_numpy_array(self.data_transformation_config.transformed_test_file_path,
                                     array=test_array)

            # Save the fitted preprocessor object
            save_object(self.data_transformation_config.transformed_obj_file_path, pre_processor_obj)

            # Create and return the DataTransformationArtifact
            data_transformation_artifcat = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_obj_file_path,
                transformed_train_file_path=self.data_transformation_config.tranformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifcat

        except Exception as e:
            raise NetworkSecurityException(e, sys)
