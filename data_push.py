# importing standard libraries
import os
import sys
import json

# Loading environment variables from .env file
from dotenv import load_dotenv
import pymongo.mongo_client
load_dotenv()

# Fetch MONGO_DB variable from env variables
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

# For SSL certification verification
import certifi
ca = certifi.where()

# Import data handling libraries
import pandas as pd
import numpy as np
import pymongo

# Custom logging and exception handling
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException

# Define a class to extract, convert and push into mongodb
class NetworkDataExtract():
    def __init__(self):
        try:
            pass # Initikization placeholder
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    # convert csv data to a list of JSON-like python dictionaries
    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path) 
            data.reset_index(drop=True, inplace=True) 
            records = list(json.loads(data.T.to_json()).values()) # converts a list of records
            return records
        except Exception as e:
            raise NetworkDataExtract(e,sys)
    
    # Insert the records into mongodb
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Establish mongodb connection
            self.mongo_db_client = pymongo.MongoClient(MONGO_DB_URL)

            # Access the specified database and collection
            self.database = self.mongo_db_client[self.database]
            self.collection = self.database[self.collection]

            # Insert multiple records into the collection
            self.collection.insert_many(self.records)

            # return the number of records inserted
            return(len(self.records))

        except Exception as e:
            raise NetworkDataExtract(e,sys)

# Mian execution block
if __name__ == '__main__':
    FILE_PATH = "Network_Data\phisingData.csv" # Path to the input csv file
    DATABASE = "JanaAi" # Target Mongodb database
    collection = "NetworkSecurity" # Target Mongodb collection
    networkobj = NetworkDataExtract() # Create instance of data handler

    # convert csv to records
    records = networkobj.cv_to_json_converter(file_path=FILE_PATH)
    # insert records into mongodb
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, collection)
    #output the number of inserted records
    print(no_of_records)
