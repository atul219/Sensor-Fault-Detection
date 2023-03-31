from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
import os, sys



if __name__ == '__main__':
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()

    # mongo_db_client = MongoDBClient()
    # print(mongo_db_client.database.list_collection_names())
    # test_exception()