from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artificat_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.utils import read_yaml_file, write_yaml_file

from sensor.exception import SensorException
from sensor.logger import logging

import pandas as pd
import os, sys

class DataValidation:

    def __init__(self,data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame)-> bool:
        # sourcery skip: class-extract-method
        """TO check if number of columns are equal in dataframe (exported from database) and in schema file

        Args:
            dataframe (pd.DataFrame): pandas DataFrame of exported data

        Raises:
            SensorException: Custom Exception

        Returns:
            bool: False if columns are not equal and True if columns are equal
        """
        try:
            logging.info('Data validation for number of columns has started')
            number_of_columns = self._schema_config['columns']
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            logging.error('Error during data validation of number of columns')
            raise SensorException(e, sys) from e

    def is_numerical_column_exist(self, dataframe: pd.DataFrame)-> bool:
        try:
            logging.info('Data validation for numerical column exist')
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns

            numerical_col_present = True
            missing_numerical_columns = []
            for num_col in numerical_columns:
                if num_col not in dataframe_columns:
                    numerical_col_present = False
                    missing_numerical_columns.append(num_col)
            
            return numerical_col_present
        except Exception as e:
            logging.error('Error during data validation of numerical column exist')
            raise SensorException(e, sys) from e

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys) from e


    def detect_data_drift(self):
        pass
    
    def initiate_data_validation(self):  # sourcery skip: raise-specific-error
        try:
            logging.info('Starting data validation')
            error_message = ''
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # reading data from traina and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ############################
            # validate number of columns
            ############################
            
            status = self.validate_number_of_columns(dataframe = train_dataframe)
            if not  status:
                error_message = f"{error_message} Train dataframe does not contain all columns"
            
            status = self.validate_number_of_columns(dataframe = test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all columns"

            ##################################
            # validate numerical columns exist
            ##################################

            status = self.is_numerical_column_exist(dataframe = train_dataframe)
            if not  status:
                error_message = f"{error_message} Train dataframe does not contain all numerical columns"
            
            status = self.is_numerical_column_exist(dataframe = test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all numerical columns"
            
            if len(error_message)> 0:
                raise Exception(error_message)
            
            # check data drift

            
        except Exception as e:
            raise SensorException(e, sys) from e