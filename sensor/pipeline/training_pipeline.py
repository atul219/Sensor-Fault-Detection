from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artificat_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

from sensor.exception import SensorException
from sensor.logger import logging
import os, sys



class TrainPipeline:
    is_pipeline_running = False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info('Starting Data Ingestion for training pipeline')
            data_ingestion_config = DataIngestionConfig(training_pipeline_config = self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingeston Completed and artifact: {data_ingestion_artifact} for training pipeline")
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_data_validation(self, data_ingestion_artifcat: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info('Starting Data Validation for training pipeline')
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config, data_ingestion_artifcat)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and artifact: {data_validation_artifact} for training pipeline")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info('Starting Data Transformation')
            data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed and artifact: {data_transformation_artifact} for training pipeline")

            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact)-> ModelTrainerArtifact:
        try:
            logging.info('Starting Model Trainer')
            model_trainer_config = ModelTrainerConfig(training_pipeline_config = self.training_pipeline_config)
            model_trainer= ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Completed and artifact: {model_trainer_artifact} for training pipeline")

            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_model_evaluation(self, data_validation_artifact, model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info('Starting Model Evaluation')
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config = self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config, data_validation_artifact, model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation Completed and artifact: {model_evaluation_artifact} for training pipeline")

            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            logging.info('Starting Model Pusher')
            model_pusher_config = ModelPusherConfig(training_pipeline_config = self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info(f"Model Pusher Completed and artifact: {model_pusher_artifact} for training pipeline")

            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        

    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("trained Model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)

            TrainPipeline.is_pipeline_running = False
        except Exception as e:
            TrainPipeline.is_pipeline_running = False
            raise SensorException(e, sys) from e