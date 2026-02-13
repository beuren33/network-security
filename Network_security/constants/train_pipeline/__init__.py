import os
import pandas as pd
import sys
import numpy as np

#Data Ingestion

TRAGET_COLUMN='Result'
PIPELINE_NAME:str = "Network_security"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str = "phishingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")
 
DATA_INGESTION_COLLECTION_NAME:str = "Network_data"
DATA_INGESTION_DATABASE_NAME:str = "Beurenpy"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTION_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.3

# Data Validation

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"