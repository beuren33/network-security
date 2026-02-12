from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.artifact_entity import DataIngestionArtifact
import os 
import sys
from typing import List
import pymongo
from sklearn.model_selection import train_test_split
import numpy as np
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_df(self):
        try:
            self.data_base_name = self.data_ingestion_config.database_name
            self.collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[self.data_base_name][self.collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(feature_store_path)
            os.makedirs(dir_name,exist_ok=True)
            dataframe.to_csv(feature_store_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info("Train Test Split is start")
            train_set, test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train Test Split end")

            dir_name = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_name,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info("Train e Test saved on {dir_name}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def init_data_ingestion(self):
        try:
            dataframe = self.export_collection_df()
            dataframe = self.export_data_feature_store(dataframe)
            self.split_data_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)