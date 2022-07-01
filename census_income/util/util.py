import yaml
from census_income.exception import Acip_Exception
import os, sys

def read_yaml_file(file_path:str)->dict:
    """
    Description: This function reads the yaml file and returns the dictionary
    """
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Acip_Exception(e,sys) from e