from sensor.utils.main import load_numpy_array_data, save_object, load_object
from sensor.entity.artificat_entity import ModelPusherArtifact, ModelEvaluationArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.ml.metrics.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.exception import SensorException
from sensor.logger import logging

import os, sys
import shutil

class ModelPusher:

    def __init__(self,model_pusher_config: ModelPusherConfig,
                 model_eval_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path

            # creating model pusher dir to sace model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok= True)
            shutil.copy(src = trained_model_path, dst = model_file_path)

            # saved_model_dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok= True)
            shutil.copy(src = trained_model_path, dst = saved_model_path)

            # prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_dir=saved_model_path,
                          model_file_path = model_file_path)
            
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")

            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
