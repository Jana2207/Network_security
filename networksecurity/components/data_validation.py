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
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig,
                 ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def ensure_directory_exist(file_path) -> None:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
    def vaidate_number_of_columns(self, dataframe:pd.DataFrame) -> bool :
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required number of columns: {number_of_columns} ")
            logging.info(f"Available number of columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_numerical_columns(self, datafram:pd.DataFrame) -> bool:
        try:
            required_int_columns = self.schema_config.get("numerical_columns", [])
            required_number_of_numerical_columns = len(required_int_columns)
            logging.info(f"Required number of numerical columns: {required_number_of_numerical_columns}")
            actual_int_columns = datafram.select_dtypes(include=['int64','int32']).columns.tolist()
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

    def validate_data_drift(self, base_dataframe, curent_dataframe, threshold = 0.05) -> bool:
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
                    "p_value":float(test_result.pvalue),
                    "drift_status":column_drift
                }
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name, exist_ok=True)
            write_yaml_file(file_path= drift_report_file_path, content=report)
            return drift_found
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataIngestionArtifact:
        try:    
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading data from file path
            train_data_frame = DataValidataion.read_data(train_file_path)
            test_data_frame = DataValidataion.read_data(test_file_path)

            # Validating number of columns
            status = self.vaidate_number_of_columns(train_data_frame)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.vaidate_number_of_columns(test_data_frame)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"
            
            # Validation of number of numerical columns
            if not self.validate_number_of_numerical_columns(train_data_frame):
                error_message=f"Train dataframe does not contain all numerical columns.\n"
            if not self.validate_number_of_numerical_columns(test_data_frame):
                error_message=f"TEst dataframe does not contain all numerical columns.\n"
            
            # Validating data drift
            drift_found = self.validate_data_drift(base_dataframe=train_data_frame, 
                                              curent_dataframe=test_data_frame)
            if drift_found:
                output_train_file_path = self.data_validation_config.invalid_train_file_path
                output_test_file_path = self.data_validation_config.invalid_test_file_path
            else:
                output_train_file_path = self.data_validation_config.valid_train_file_path
                output_test_file_path = self.data_validation_config.valid_test_file_path
            
            # Ensure directory exist
            DataValidataion.ensure_directory_exist(output_train_file_path)
            DataValidataion.ensure_directory_exist(output_test_file_path)

            # Save dataframes
            train_data_frame.to_csv(output_train_file_path, index = False, header = True)
            test_data_frame.to_csv(output_test_file_path, index = False, header = True)

            # Create the final artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status = not drift_found,
                valid_train_file_path = output_train_file_path if not drift_found else None, 
                valid_test_file_path = output_test_file_path if not drift_found else None,
                invalid_train_file_path = output_train_file_path if drift_found else None,
                invalid_test_file_path = output_test_file_path if drift_found else None,
                drift_report_file_path = self.data_validation_config
            )
            return data_validation_artifact           
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

        