from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import os, sys
import pandas as pd

class DataValidataion:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            # Load schema configuration for validation
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads CSV data into a pandas DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def ensure_directory_exist(file_path) -> None:
        """
        Ensures the directory for a given file path exists.
        """
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

    def vaidate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates whether the number of columns in the DataFrame
        matches the schema definition.
        """
        try:
            columns_list = self.schema_config['columns']
            columns_dict = {k: v for d in columns_list for k, v in d.items()}
            number_of_columns = len(columns_dict)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Available number of columns: {len(dataframe.columns)}")
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_numerical_columns(self, datafram: pd.DataFrame) -> bool:
        """
        Validates the presence and count of numerical columns as per schema.
        Logs missing or extra columns.
        """
        try:
            required_int_columns = self.schema_config.get("numerical_columns", [])
            required_number_of_numerical_columns = len(required_int_columns)
            logging.info(f"Required number of numerical columns: {required_number_of_numerical_columns}")
            
            actual_int_columns = datafram.select_dtypes(include=['int64', 'int32']).columns.tolist()
            actual_number_of_numerical_columns = len(actual_int_columns)
            logging.info(f"Available number of numerical columns: {actual_number_of_numerical_columns}")

            missing_columns = list(set(required_int_columns) - set(actual_int_columns))
            extra_columns = list(set(actual_int_columns) - set(required_int_columns))

            if required_number_of_numerical_columns == actual_number_of_numerical_columns:
                return True
            else:
                logging.info(f"Missing columns: {missing_columns}")
                logging.info(f"Extra columns: {extra_columns}")
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_data_drift(self, base_dataframe, curent_dataframe, threshold=0.05) -> bool:
        """
        Detects data drift using the Kolmogorov-Smirnov test.
        Saves the drift report to a YAML file.
        Returns True if drift is found in any column.
        """
        try:
            drift_found = False
            report = {}

            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = curent_dataframe[column]
                test_result = ks_2samp(d1, d2)

                column_drift = test_result.pvalue < threshold
                if column_drift:
                    drift_found = True

                report[column] = {
                    "p_value": float(test_result.pvalue),
                    "drift_status": column_drift
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return drift_found
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Runs the complete data validation process:
        - Reads training and testing datasets
        - Validates schema (column count and numerical columns)
        - Checks for data drift
        - Saves valid or invalid datasets accordingly
        - Returns a DataValidationArtifact with metadata
        """
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the datasets
            train_data_frame = DataValidataion.read_data(train_file_path)
            test_data_frame = DataValidataion.read_data(test_file_path)

            # Validate number of columns
            if not self.vaidate_number_of_columns(train_data_frame):
                logging.warning("Train dataframe does not contain all columns as per schema.")
            if not self.vaidate_number_of_columns(test_data_frame):
                logging.warning("Test dataframe does not contain all columns as per schema.")

            # Validate number of numerical columns
            if not self.validate_number_of_numerical_columns(train_data_frame):
                logging.warning("Train dataframe does not contain all required numerical columns.")
            if not self.validate_number_of_numerical_columns(test_data_frame):
                logging.warning("Test dataframe does not contain all required numerical columns.")

            # Validate data drift
            drift_found = self.validate_data_drift(base_dataframe=train_data_frame,
                                                   curent_dataframe=test_data_frame)

            # Determine file paths for saving validated datasets
            if drift_found:
                output_train_file_path = self.data_validation_config.invalid_train_file_path
                output_test_file_path = self.data_validation_config.invalid_test_file_path
            else:
                output_train_file_path = self.data_validation_config.valid_train_file_path
                output_test_file_path = self.data_validation_config.valid_test_file_path

            # Ensure output directories exist
            DataValidataion.ensure_directory_exist(output_train_file_path)
            DataValidataion.ensure_directory_exist(output_test_file_path)

            # Save validated datasets
            train_data_frame.to_csv(output_train_file_path, index=False, header=True)
            test_data_frame.to_csv(output_test_file_path, index=False, header=True)

            # Create and return the artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=not drift_found,
                valid_train_file_path=output_train_file_path if not drift_found else None,
                valid_test_file_path=output_test_file_path if not drift_found else None,
                invalid_train_file_path=output_train_file_path if drift_found else None,
                invalid_test_file_path=output_test_file_path if drift_found else None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
