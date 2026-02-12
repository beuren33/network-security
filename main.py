from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.components.data_ingestion import DataIngestion
from Network_security.entity.config_entity import DataIngestionConfig,TrainPipelineConfig
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting Data Ingestion")
        data_ingestion_artifact=data_ingestion.init_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)