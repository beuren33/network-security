from sklearn.model_selection import GridSearchCV
import yaml
from Network_security.exception.exception import NetworkSecurityException
import os,sys
from Network_security.logging.logger import logging
import numpy as np
import dill
import pickle

from Network_security.utils.ml_util.metric.classification_metric import get_classification_score


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path:str,obj):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"O arquivo {file_path} nao existe")
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def models_evaluate(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}

        for i in range(len(list(models))):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]

            gs = GridSearchCV(model,param,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_test_pred = model.predict(x_test)

            test_model_score=get_classification_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)