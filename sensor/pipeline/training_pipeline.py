from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artificat_entity import DataIngestionArtifact
from sensor.components.data_ingestion import DataIngestion

from sensor.exception import SensorException
from sensor.logger import logging
import os, sys

class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config = self.training_pipeline_config)


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info('Starting Data Ingestion for training pipeline')
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingeston Completed and artifact: {data_ingestion_artifact} for training pipeline")
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e, sys) from e
        
    
    def start_data_validation(self):
        try:
            pass
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
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e, sys) from e