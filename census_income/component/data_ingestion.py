
from census_income.entity.config_entity import DataIngestionConfig
from census_income.logger import logging
from census_income.exception import Acip_Exception
import os, sys
import pandas as pd
import numpy as np
from six.moves import urllib
from census_income.entity.config_entity import DataIngestionConfig
from census_income.entity.artifact_entity import  DataIngestionArtifact
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*30} Data ingestion started {'='*30}")
            self.data_ingestion_config=data_ingestion_config
        
        except Exception as e:
            raise Acip_Exception(e,sys) from e
        
    def download_census_data(self):
        try:
            # Downloading the census data url
            download_url = self.data_ingestion_config.dataset_download_url
            
            # Folder location where the census data is to be downloaded
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
                
            # create the folder if it does not exist
            os.makedirs(raw_data_dir, exist_ok=True)
            
            # Filename of the downloaded census data
            census_file_name = os.path.basename(download_url)
            
            # File path of the downloaded census data
            census_file_path = os.path.join(raw_data_dir, census_file_name)
            
            # Downloading the census data
            logging.info(f"Downloading the census data from [ {download_url} ] into [ {census_file_path} ]")
            urllib.request.urlretrieve(download_url, census_file_path)
            logging.info(f"Dataset downloaded successfully [ {census_file_path} ] ")
            
            return census_file_path
            
            
        except Exception as e:
            raise Acip_Exception(e,sys) from e
        
        
    def split_data_as_train_test(self) ->DataIngestionArtifact:
        try:
            # Raw census data file path
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            # Census data file name
            file_name = os.listdir(raw_data_dir)[0]
            
            # Census data file path
            census_file_path = os.path.join(raw_data_dir, file_name)
            
            # Census data file
            logging.info(f"Reading the census data from [ {census_file_path} ]")
            census_data_frame = pd.read_csv(census_file_path, low_memory=False)
            
            census_data_frame["income_bracket"] = census_data_frame["salary"].apply(lambda x: ">50K" if x == ">50K." else "<=50K")
            
            # Census data file shape
            strat_train_set = None
            strat_test_set = None
            
            # Stratified split of the census data
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            
            # Iterating over the stratified split
            for train_index, test_index in split.split(census_data_frame, census_data_frame["income_bracket"]):
                strat_train_set = census_data_frame.loc[train_index].drop(["income_bracket"], axis=1)
                strat_test_set = census_data_frame.loc[test_index].drop(["income_bracket"], axis=1)
                
            # Creating the train and test data artifacts    
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)
            
            # Writing the train data artifacts
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Saving the train data to {train_file_path}")
                strat_train_set.to_csv(train_file_path, index=False)
                
            # Writing the test data artifacts    
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Saving the test data to {test_file_path}")
                strat_test_set.to_csv(test_file_path, index=False)
                
            # Creating the data ingestion artifact    
            Data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested= True,
                                                            message= "Data ingested successfully")
            
            logging.info(f"Data Ingestion Artifact : [{Data_ingestion_artifact}]")
            
            # Returning the data ingestion artifact
            return Data_ingestion_artifact
        
        except Exception as e:
            raise Acip_Exception(e,sys) from e
        
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        try:
            # Downloading the census data
            census_file_path = self.download_census_data()
            
            # Splitting the census data
            data_ingestion_artifact = self.split_data_as_train_test()
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise Acip_Exception(e,sys) from e
        
    def __del__(self):
        try:
            logging.info(f"{'='*30} Data ingestion completed {'='*30}\n\n")
        except Exception as e:
            raise Acip_Exception(e,sys) from e
