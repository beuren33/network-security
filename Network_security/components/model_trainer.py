import sys
import os
from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import TrainerModelConfig
from Network_security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from Network_security.components.data_ingestion import DataIngestion
from Network_security.utils.main_util import load_numpy_array,save_object,load_object,models_evaluate
from Network_security.components.data_validation import DataValidation
from Network_security.utils.ml_util.model.estimator import NetworkModel
from Network_security.utils.ml_util.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier)


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,trainer_model_config:TrainerModelConfig):
        try:
            self.model_trainer_config = trainer_model_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                "LogisticRegression":LogisticRegression(verbose=1),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "RandomForestClassifier":RandomForestClassifier(verbose=1),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "GradientBoostingClassifier":GradientBoostingClassifier()
            }
            params={
                "LogisticRegression":{
                    'C': [1.0],
                    'penalty': ['l2'],
                    'solver': ['lbfgs']
                },
                "DecisionTreeClassifier":{
                    'criterion': ['gini', 'entropy','log_loss']
                },
                "RandomForestClassifier":{
                    'n_estimators': [8,16,32,64,128,256],
                },
                "AdaBoostClassifier":{
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 1]
                },
                "GradientBoostingClassifier":{
                    'n_estimators': [8,16,32,64,128,256],
                    'learning_rate': [.1,.01,.05,.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9]
                }
            }
            report: dict = models_evaluate(x_train, y_train, x_test, y_test, models, params)

            f1_scores_list = [artifact.f1_score for artifact in report.values()] 
            
            best_model_score = max(f1_scores_list)

            best_model_name = list(report.keys())[
                f1_scores_list.index(best_model_score)
            ]
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)

            class_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)

            y_test_pred = best_model.predict(x_test)

            class_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model =NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=network_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=class_train_metric,
                test_metric_artifact=class_test_metric
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def init_trainer_model(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            


            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

            
