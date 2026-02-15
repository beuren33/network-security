import os
import pandas as pd
import sys
import numpy as np

#Data Ingestion

TARGET_COLUMN='Result'
PIPELINE_NAME:str = "Network_security"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str = "phishingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")

SAVED_MODEL_DIR:str = "saved_models"
MODEL_FILE_NAME:str = "model.pkl"
 
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

#Data Transformation

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict ={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH:str ="train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH:str ="test.npy"
#Model Training

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str= "model.pkl"
MODEL_TRANER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD:float = 0.05


