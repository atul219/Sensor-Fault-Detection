from sensor.utils.main import load_numpy_array_data, save_object, load_object
from sensor.entity.artificat_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.ml.metrics.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.exception import SensorException
from sensor.logger import logging

import sys, os

from xgboost import XGBClassifier
from sklearn import svm

class ModelTrainer:

    def __init__(self, mdoel_trainer_config: ModelTrainerConfig, 
                 data_transofrmation_artifact: DataTransformationArtifact):
        
        try:
            self.model_trainer_config = mdoel_trainer_config
            self.data_transofrmation_artifact = data_transofrmation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
    
    def perform_hyperparameterization(self):
        pass

    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        
        except Exception as e:
            raise SensorException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:
            train_file_path = self.data_transofrmation_artifact.transformed_train_file_path
            test_file_path = self.data_transofrmation_artifact.transformed_test_file_path

            # load training array
            train_arr  = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            # split feature and target column from train and test arrays
            # last column is target column 
            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1], # data except last column
                train_arr[:, -1],  # only last column
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            logging.info('Model Training')
            model = self.train_model(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            classification_train_metric = get_classification_score(y_true = y_train, y_pred = y_train_pred)
            classification_test_metric = get_classification_score(y_true = y_test, y_pred = y_test_pred)
            logging.info('Classification Score generated')
            # trained model score is low
            if classification_train_metric.f1_score <= self.model_trainer_config.expected_acc:
                raise Exception('Trained model has low score then our provided score')

            # check overfitting and underfitting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            if diff > self.model_trainer_config.over_under_thres:
                raise Exception("Model is not good try to do more experimentaion")

            preprocessor = load_object(filepath= self.data_transofrmation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_dir_name)
            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model = SensorModel(preprocessor = preprocessor, model = model)

            save_object(self.model_trainer_config.trained_model_file_path, obj = sensor_model)

            # model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                                 train_metric_artifact = classification_train_metric,
                                 test_metric_artifact = classification_test_metric)

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
