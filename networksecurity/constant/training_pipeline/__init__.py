# Importing required libraries
import os
import sys
import pandas
import numpy

# Defining the target column for the machine learning model
TARGET_COLUMN = "Result"

# Defining pipeline-level constant variables
PIPELINE_NAME: str = "NetowrkSecurity"  # Name of the overall ML pipeline
ARTIFICT_DIR: str = "Artifacts"         # Base directory for all pipeline artifacts
FILE_NAME: str = "Phising_data.csv"     # Raw data filename extracted from MongoDB
TRAIN_FILE_NAME: str = "train.csv"      # Training dataset filename
TEST_FILE_NAME: str = "test.csv"        # Testing dataset filename

# Data ingestion-related constants (used to generate directory/file paths)
DATA_INGESTION_COLLECTION_NAME: str = "NetworkSecurity"  # MongoDB collection name
DATA_INGESTION_DATABASE_NAME: str = "JanaAi"             # MongoDB database name
DATA_INGESTION_DIRECTORY_NAME: str = "data_ingestion"    # Sub-directory for ingestion artifacts
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Sub-directory for raw data
DATA_INGESTION_INGESTED_DIR: str = "ingested"            # Sub-directory for train/test splits
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2       # Train/test split ratio (train = 2x test)
