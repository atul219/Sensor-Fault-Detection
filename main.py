from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
import os, sys
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main import load_object


from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run


app = FastAPI()
origins = ["*"]

@app.get('/', tags = ['authentication'])
async def index():
    return RedirectResponse(url ='/docs')

@app.get('/train')
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running")
        train_pipeline.run_pipeline()

        return Response("Training successful !!")
    
    except Exception as e:
        return Response(f"Error occurred : {e}")


@app.get('/predict')
async def predictRouteClient():
    try:
        # get data from user ( csv or values)
        # convert csv to dataframe
        df = None
        model_resolver = ModelResolver(model_dir= SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path= best_model_path)

        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(), inplace = True)

        # decide how to return the data
        #  
    except Exception as e:
        return Response(f"Error occurred : {e}")


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)
    # http://localhost:8080/docs     this will work


    
# if __name__ == '__main__':
#     try:
#         train_pipeline = TrainPipeline()
#         train_pipeline.run_pipeline()
#     except Exception as e:
#         raise (e)


    # mongo_db_client = MongoDBClient()
    # print(mongo_db_client.database.list_collection_names())
    # test_exception()