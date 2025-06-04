# Importing required libraries
import os
import sys
import pandas as pd
import numpy as np

# Defining the target column for the machine learning model
TARGET_COLUMN = "Result"

# Defining pipeline-level constant variables
PIPELINE_NAME: str = "NetowrkSecurity"  # Name of the overall ML pipeline
ARTIFICT_DIR: str = "Artifacts"         # Base directory for all pipeline artifacts
FILE_NAME: str = "Phising_data.csv"     # Raw data filename extracted from MongoDB
TRAIN_FILE_NAME: str = "train.csv"      # Training dataset filename
TEST_FILE_NAME: str = "test.csv"        # Testing dataset filename
SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")   # Data schema file path

# Data ingestion-related constants (used to generate directory/file paths)
DATA_INGESTION_COLLECTION_NAME: str = "NetworkSecurity"  # MongoDB collection name
DATA_INGESTION_DATABASE_NAME: str = "JanaAi"             # MongoDB database name
DATA_INGESTION_DIRECTORY_NAME: str = "data_ingestion"    # Sub-directory for ingestion artifacts
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Sub-directory for raw data
DATA_INGESTION_INGESTED_DIR: str = "ingested"            # Sub-directory for train/test splits
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2       # Train/test split ratio (train = 2x test)

# Data validation-related constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"           # Directory for validation data
DATA_VALIDATION_VALID_DIR: str = "validated"                # Sub-directory for valid data    
DATA_VALIDATION_INVALID_DIR: str = "invalid"                # Sub-directory for invalid data
DATA_VALIDATION_DRIFT_REPODT_DIR: str = "drift_report"      # Sub-directory for drift report  
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml" # Drift report file name

# Data Transformation related constants
DATA_TRANSFORMATION_DIR_NAME: str = "transformation"                    # Directory for data transformation
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"           # Directory for transformed data
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"  # directory for transformed object
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"                  # Transformed train numpy array file path         
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"                    # Transformed test numpy array file path
PRE_PROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"              # transfromed object file file path
## Parameters for KNN imputer
DATA_TRANSFORMATION_IMPUTER_PARAMETERS: dict ={                     
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}