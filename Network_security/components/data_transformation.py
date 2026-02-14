import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from Network_security.entity.config_entity import DataTransformationConfig
from Network_security.constants.train_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_security.utils.main_util import save_object, save_numpy_array


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def get_transformer_object(cls)->Pipeline:
        logging.info('Iniciando o metodo transformer object de DataTransformation')
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Init KNNInputer com os parametros: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline=Pipeline([
                ('imputer',imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

    def init_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Start Data Traansformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Read train e test completo")

            rm_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            rm_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_transformer_object()
            preprocessor_obj=preprocessor.fit(rm_feature_train_df)
            transformed_rm_feature_train_df=preprocessor_obj.transform(rm_feature_train_df)
            transformed_rm_feature_test_df=preprocessor_obj.transform(rm_feature_test_df)

            train_arr=np.c_[transformed_rm_feature_train_df,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_rm_feature_test_df,np.array(target_feature_test_df)]

            save_numpy_array(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.preprocessed_object_file_path,obj=preprocessor_obj)

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.preprocessed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)