from Network_security.logging.logger import logging
from Network_security.exception.exception import NetworkSecurityException
from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DataTransformation
from Network_security.entity.config_entity import DataIngestionConfig,TrainPipelineConfig,DataValidationConfig,DataTransformationConfig
import sys

if __name__ == "__main__":
    try:
        #INGESTION
        training_pipeline_config = TrainPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting Data Ingestion")
        data_ingestion_artifact=data_ingestion.init_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)

        #VALIDATION
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Starting Data Validation")
        data_validation_artifact = data_validation.init_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

        #TRANSFORMATION
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Starting Data Transformation")
        data_transformation_artifact=data_transformation.init_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)