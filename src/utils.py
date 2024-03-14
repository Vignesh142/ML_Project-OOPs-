import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path= os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
            
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(X_train, y_train, X_test, y_test, models, params):
        try:
            model_report = {}
            for model_name, model in models.items():

                param = params[model_name]
                
                gs= GridSearchCV(model, param, cv=5, n_jobs=-1, verbose=1)
                gs.fit(X_train, y_train)
                
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)
                
                y_train_pred = model.predict(X_train)
                
                y_test_pred = model.predict(X_test)
                
                train_model_score= r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)
                
                model_report[model_name] = test_model_score
            return model_report
        
        except Exception as e:
            raise CustomException(e, sys)
        
def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise CustomException(e, sys)