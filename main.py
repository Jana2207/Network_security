# Import custom logging, exception handling, and required pipeline components
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipeConfig, DataValidationConfig
from networksecurity.components.data_validation import DataValidataion
import sys

# Entry point for the data ingestion process
if __name__ == '__main__':
    try:
        # Initialize overall training pipeline configuration
        trainingpipelineconfig = TrainingPipeConfig()

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


    except Exception as e:
        # Raise custom exception with detailed traceback for better debugging
        raise NetworkSecurityException(e, sys)
