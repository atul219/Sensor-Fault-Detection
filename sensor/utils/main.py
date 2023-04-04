from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import yaml
import numpy as np
import dill

def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise SensorException(e, sys) from e
    

def write_yaml_file(filepath: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(filepath):
            os.remove(filepath)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as yaml_file:
            yaml.dump(content, yaml_file)


    except Exception as e:
        raise SensorException(e, sys) from e
    

def save_numpy_array_data(filepath: str, array: np.array):
    """save numpy array data to file

    Args:
        filepath (str): _description_
        array (np.array): _description_
    """

    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'wb') as file_obj:
            np.save(file_obj, array)
    
    except Exception as e:
        raise SensorException(e, sys) from e
    

def load_numpy_array_deta(filepath: str) -> np.array:
    """laod numpy array data from file

    Args:
        filepath (str): _description_

    Returns:
        np.array: _description_
    """
    try:
        logging.info('Loadinng Numpy  array data')
        with open(filepath, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
    

def save_object(filepath: str, obj: object) -> None:

    try:
        logging.info('Saving Object')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        
        logging.info('Object Saved')
    except Exception as e:
        raise SensorException(e, sys) from e
    