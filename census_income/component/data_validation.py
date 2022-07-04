from census_income.logger import logging
from census_income.exception import Acip_Exception
from census_income.entity.config_entity import DataValidationConfig
from census_income.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os,sys
import pandas as pd
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

class DataValidation:
    
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            pass
        
        except Exception as e:
            raise Acip_Exception(e, sys) from e
        
    def get_train_and_test_split(self):
        try:
            pass
        
        except