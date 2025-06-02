# Importing required modules
from datetime import datetime
import os
from networksecurity.constant import training_pipeline  # Importing the constants defined above

# Print statements for verification/debugging purposes
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFICT_DIR)

# This class generates a dynamic path structure for storing all pipeline artifacts
class TrainingPipeConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")  # Format the timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME  # e.g., "NetowrkSecurity"
        self.artifact_name = training_pipeline.ARTIFICT_DIR   # e.g., "Artifacts"
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)  # Full path to this run's artifact directory
        self.timestamp: str = timestamp  # Save formatted timestamp for traceability

# This class constructs file paths and settings needed for data ingestion
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipeConfig):
        # Main directory where data ingestion outputs are stored
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIRECTORY_NAME
        )

        # File path for the raw data fetched from MongoDB and saved as CSV
        self.future_sotre_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        # File path for the training data after the split
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        # File path for the testing data after the split
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        # Ratio to split train and test data 
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        # MongoDB collection and database names used for fetching data
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
