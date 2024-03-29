import sys
from typing import Optional
import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
from sensor.logger import logging


class SensorData:
    """This class will export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient()
        except Exception as e:
            raise SensorException(e, sys) from e
        
    def export_collection_as_datafrme(self, collection_name: str, database_name: Optional[str] = None)-> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.database[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df
        except Exception as e:
            raise SensorException(e, sys) from e