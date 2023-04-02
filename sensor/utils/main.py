from sensor.exception import SensorException
import os, sys
import yaml

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
        
        os.makedirs(filepath)(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as yaml_file:
            yaml.dump(content, yaml_file)


    except Exception as e:
        raise SensorException(e, sys) from e