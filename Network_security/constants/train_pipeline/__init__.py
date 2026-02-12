import os
import pandas as pd
import sys
import numpy as np

TRAGET_COLUMN='Result'
PIPELINE_NAME:str = "Network_security"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str = "phishingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
 
DATA_INGESTION_COLLECTION_NAME:str = "Network_data"
DATA_INGESTION_DATABASE_NAME:str = "Beurenpy"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTION_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.3