import os
import sys
import pandas as pd
import numpy as np

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidataion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipeConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig
)

from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainingArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipeConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidataion(data_ingestion_artifact=data_ingestion_artifact,
                                              data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact:DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Data transfrmation started")
            data_trasnformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_trasnformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data transforamation completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def strat_model_traininig(self, data_transformation_artifact:DataTransformationArtifact) -> ModelTrainingArtifact:
        try:
            logging.info("Model traininig started")
            model_training_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
            model_training = ModelTrainer(model_training_config=model_training_config,
                                          data_transformation_artifact=data_transformation_artifact)
            model_training_artifact = model_training.initiate_model_training()
            logging.info(f"Model training completed and artifact: {model_training_config}")
            return model_training_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.strat_model_traininig(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    