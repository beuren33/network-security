import os
import sys
from Network_security.logging.logger import logging
from Network_security.exception.exception import NetworkSecurityException
from dotenv import load_dotenv
import certifi
from Network_security.utils.ml_util.model.estimator import NetworkModel
import pymongo
from Network_security.pipeline.trainer_pipeline import TrainPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from Network_security.utils.main_util import load_object
from Network_security.constants.train_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

load_dotenv()
ca = certifi.where()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db=client[DATA_INGESTION_DATABASE_NAME]
collection=db[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training success")
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post('/predict')
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)

        preprocessor=load_object("final_models/preprocessing.pkl")
        model=load_object("final_models/model.pkl")

        network_model = NetworkModel(preprocessor=preprocessor,model=model)
        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)

        df['prediction']=y_pred
        print(df["prediction"])
        df.to_csv("prediction_output/prediction.csv",index=False)

        table_html=df.to_html(classes='table table-striped')

        return templates.TemplateResponse("index.html",{"request":request,"table":table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)