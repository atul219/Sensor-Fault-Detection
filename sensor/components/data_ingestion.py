from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artificat_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main import read_yaml_file

from sklearn.model_selection import train_test_split

import sys, os
import pandas as pd

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise SensorException(e, sys) from e
    
    def export_data_into_feature_store(self)-> pd.DataFrame:
        """Export mongo db collecrion record as dataframe into feature store dir

        Returns:
            pd.Dataframe: pandas dataframe
        """
        try:
            logging.info("Exporting Data from MongoDB into feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_datafrme(collection_name= self.data_ingestion_config.collection_name)

            # get feature store file path from config entity data ingestion class
            feature_store_file_path = self.data_ingestion_config.ferature_store_file_path

            # create directory
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # save data to feature store
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            
            return dataframe

        except Exception as e:
            raise SensorException(e, sys) from e

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """exported data from feature store will be divided into train and test file

        Args:
            dataframe (pd.DataFrame): _description_
        """
        try:
            logging.info('Train and Test data splitting started')
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info('Performed train test split on the dataframe')
            logging.info('Exited split_data_as_train_test method of Data_Ingestion class')

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)

            test_set.to_csv(self.data_ingestion_config.test_file_path, index = False, header = True)

            logging.info("Exported train and test file path")                    

        except Exception as e:
            raise SensorException(e, sys) from e
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            dataframe = dataframe.drop(self._schema_config["drop_columns"], axis = 1)
            self.split_data_as_train_test(dataframe = dataframe)

            return DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
        except Exception as e:
            raise SensorException(e, sys) from e