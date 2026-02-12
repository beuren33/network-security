import json
import os
import sys
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy
import pymongo
from Network_security.logging.logger import logging
from Network_security.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def extract_data(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records= list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_mongodb (self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.db = self.mongo_client[self.database]

            self.collection= self.db[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH='Network_data\phisingData.csv'
    DATABASE= 'Beurenpy'
    Collection ='Network_data'
    obj=NetworkDataExtract()
    records = obj.extract_data(file_path=FILE_PATH)
    nm_records=obj.insert_data_mongodb(records,DATABASE,Collection)
    print(nm_records)
    print(records)

