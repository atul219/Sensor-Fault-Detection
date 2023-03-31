from datetime import datetime
import os
from sensor.constant.training_pipeline import (PIPELINE_NAME, 
                                            ARTIFACT_DIR, 
                                            DATA_INGESTION_DIR_NAME, 
                                            DATA_INGESTION_FEATURE_STORE_DIR, 
                                            DATA_INGESTION_INGESTED_DIR, 
                                            FILE_NAME,
                                            TRAIN_FILE_NAME,
                                            TEST_FILE_NAME,
                                            DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
                                            DATA_INGESTION_COLLECTION_NAME)


# In artifact folder timestamp folder will be created where all the data ingestion and etc folder will be stored with timestamps because we might want to train our model again
class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):

        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifcat_dir: str = os.path.join(ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp


# Data Ingestion Config
# define all the paths of following directory or file

class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifcat_dir, DATA_INGESTION_DIR_NAME)

        self.ferature_store_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)

        self.training_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)

        self.test_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)

        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME