import os
import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi

ca =certifi.where()

class MongoDBClient:
    client = None

    def __init__(self,database_name = DATABASE_NAME)->None:
        # sourcery skip: raise-specific-error
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv('MONGODBURL')
                if mongo_db_url is None:
                    raise Exception(f'Environment Key: {mongo_db_url} is not set.')
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise e
            # raise SensorException(e, sys)

