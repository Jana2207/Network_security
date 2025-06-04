from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    """
    DataIngestion handles the entire data ingestion process:
    - Extracts data from MongoDB
    - Stores it in a feature store (CSV file)
    - Splits it into training and testing datasets
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initializes the DataIngestion object with configuration.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collections_as_dataframe(self) -> pd.DataFrame:
        """
        Connects to MongoDB, retrieves data from the specified collection, and returns it as a pandas DataFrame.
        Removes the '_id' column if it exists and replaces 'na' strings with np.nan.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            # Convert MongoDB collection to DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop MongoDB default ID field
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], axis=1, inplace=True)

            # Replace string 'na' with actual NaN
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Saves the cleaned DataFrame into a CSV file called the feature store.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.future_sotre_file_path

            # Ensure directory exists
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save DataFrame to CSV
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Splits the dataset into training and testing sets and saves them as separate CSV files.
        """
        try:
            # Perform train-test split
            trainset, testset = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=7
            )

            logging.info("Performed train-test split on the data.")
            logging.info("Exited split_data_as_train_test method from DataIngestion.")

            # Ensure target directory exists
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file paths.")

            # Save datasets
            trainset.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            testset.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info("Exported train and test file paths.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Executes the complete data ingestion pipeline and returns artifact containing paths to train/test files.
        """
        try:
            # Step 1: Load data from MongoDB
            dataframe = self.export_collections_as_dataframe()

            # Step 2: Save data to feature store
            dataframe = self.export_data_into_feature_store(dataframe)

            # Step 3: Split and save train/test data
            self.split_data_as_train_test(dataframe)

            # Step 4: Return artifact with paths to output files
            dataingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return dataingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
