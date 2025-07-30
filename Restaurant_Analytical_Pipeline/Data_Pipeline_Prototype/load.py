import os
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import logging

class load():
   
    def __init__(self):

        api = KaggleApi()
        api.authenticate()
        logging.info('downloading yelp dataset...')
        api.dataset_download_files('yelp-dataset/yelp-dataset')
        path = os.getcwd() + '/yelp-dataset.zip'
        with ZipFile(path, 'r') as zipObj:
            zipObj.extractall()

