# Import custom logging, exception handling, and required pipeline components
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import(
    DataIngestionConfig, 
    TrainingPipeConfig, 
    DataValidationConfig,
    DataTransformationConfig)
from networksecurity.components.data_validation import DataValidataion
from networksecurity.components.data_transformation import DataTransformation
import sys

# Entry point for the data ingestion process
if __name__ == '__main__':
    try:
        # Initialize overall training pipeline configuration
        trainingpipelineconfig = TrainingPipeConfig()

        logging.info("Starting the Data ingestion")
        # Create specific configuration for data ingestion using the training pipeline config
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)

        # Initialize the DataIngestion component with the configuration
        datainjestion = DataIngestion(dataingestionconfig)

        # Log the start of the data ingestion process
        logging.info("Initiating the data ingestion process.")

        # Trigger the complete data ingestion pipeline (MongoDB -> Feature Store -> Train/Test Split)
        datainjestionartifact = datainjestion.initate_data_ingestion()

        # Output the paths to the generated train and test datasets
        print(datainjestionartifact)
        logging.info("Data ingestion completed")

        logging.info("Starting the data validation")
        # Create DataValidationConfig object using the training pipeline configuration
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)

        # Initialize the DataValidataion class with data ingestion artifacts and validation config
        datavalidation = DataValidataion(datainjestionartifact, datavalidationconfig)

        # Log the beginning of the data validation process
        logging.info("Initiating the data validation")

        # Trigger the data validation process and get the resulting artifact
        datavalidationartifact = datavalidation.initiate_data_validation()

        # Print the DataValidationArtifact object to verify validation results
        print(datavalidationartifact)
        logging.info("Data validation completed")

        logging.info("Starting the data transformation")
        # Creating Data transformation object
        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        datatransformation = DataTransformation(datavalidationartifact, datatransformationconfig)
        datatransformationartifact = datatransformation.initiate_data_transformation()
        print(datatransformationartifact)
        logging.info("Data transformation competed")

    except Exception as e:
        # Raise custom exception with detailed traceback for better debugging
        raise NetworkSecurityException(e, sys)
