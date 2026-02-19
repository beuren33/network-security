import os
import sys
from Network_security.logging.logger import logging
from Network_security.exception.exception import NetworkSecurityException
from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DataTransformation
from Network_security.components.model_trainer import ModelTrainer
from Network_security.entity.config_entity import (
    TrainPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    TrainerModelConfig,
)
from Network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

class TrainPipeline:
    def __init__(self):
        self.train_pipeline_config = TrainPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(train_pipeline_config=self.train_pipeline_config)
            logging.info("Start data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.init_data_ingestion()
            logging.info("Complete data ingestion")

            return data_ingestion_artifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(train_pipeline_config=self.train_pipeline_config)
            logging.info("Start data validation")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.init_data_validation()
            logging.info("Complete data validation")

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        self.data_transformation_config = DataTransformationConfig(train_pipeline_config=self.train_pipeline_config)
        logging.info("Start data transformation")
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
        data_transformation_artifact = data_transformation.init_data_transformation()
        logging.info("Complete data transformation")

        return data_transformation_artifact
    
    def start_trainer_model(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config: TrainerModelConfig = TrainerModelConfig(train_pipeline_config=self.train_pipeline_config)
            logging.info("Start Model Trainer")

            model_trainer = ModelTrainer(data_transformation_artifact,self.model_trainer_config)

            model_trainer_artifact = model_trainer.init_trainer_model()
            logging.info("Complete Model Trainer")

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()

            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)

            model_trainer_artifact:ModelTrainerArtifact = self.start_trainer_model(data_transformation_artifact=data_transformation_artifact)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)