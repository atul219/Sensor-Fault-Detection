from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from sensor.entity.artificat_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation

from sensor.exception import SensorException
from sensor.logger import logging
import os, sys

class TrainPipeline:
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
        
    
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys) from e
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
        except Exception as e:
            raise SensorException(e, sys) from e