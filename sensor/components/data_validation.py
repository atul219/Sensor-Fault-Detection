from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artificat_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.utils.main import read_yaml_file, write_yaml_file

from sensor.exception import SensorException
from sensor.logger import logging


from scipy.stats import ks_2samp

import pandas as pd
import os, sys

class DataValidation:

    def __init__(self,
                 data_validation_config: DataValidationConfig, 
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame)-> bool:
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
            number_of_columns = len(self._schema_config['columns'])
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            logging.error('Error during data validation of number of columns')
            raise SensorException(e, sys) from e

    def is_numerical_column_exist(self, dataframe: pd.DataFrame)-> bool:
        try:
            logging.info('Data validation for numerical column exist Started')
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


    def detect_data_drift(self, train_df, test_df, threshold = 0.05)-> bool:
        
        try:
            logging.info('Checking data drift Started')
            status = True
            report = {}
            for column in train_df.columns:
                data_1 = train_df[column]
                data_2 = test_df[column]
                is_same_dist = ks_2samp(data_1, data_2)

                if threshold <= is_same_dist.pvalue:
                    drift_found = False
                else:
                    drift_found = True
                    status = False
                report[column] = {
                    'p_value': float(is_same_dist.pvalue),
                    'drift_status': drift_found,
                }

            drift_report_file_path = self.data_validation_config.report_file_path
            
            # create dir to write yaml file
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report)

            return status
            
        except Exception as e:
            logging.error('Error while checking data drift')
            raise SensorException(e, sys) from e
    
    def initiate_data_validation(self)-> DataValidationArtifact:  # sourcery skip: raise-specific-error
        try:
            logging.info('Starting data validation')
            error_message = ''
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # reading data from train and test file location
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
            
            ##################
            # check data drift
            ##################
            status = self.detect_data_drift(train_df = train_dataframe, test_df = test_dataframe)
            
            ##########################
            # data validation artifact
            ##########################

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path= self.data_ingestion_artifact.train_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e