import json
from pathlib import Path

config_dir = '../config.json'

def decryptFile(file_name: str) -> bool:
    '''
    Decrypts the '.tms' file format to its original format.

        file_name: name of the file to be decrypted.
    '''
    ## confirm file directory and name
    assert type(file_name) == str ## remove on release
    if Path(file_name).exists() is False:
        return False
    
    ## read config.json

    ## read all data in the file
    with open(file_name, 'rb') as f:
        file = f.read()

        ## seek the inprint data

        ## extract and slice out imprint data

        ## get extension from imprint data

        ## decrypt the file with the decryption key**

        ## rewrite file in new format

def extract_config(config_dir: str, param=None):
    '''
        Collects all or some parameters from the config file.
        config_dir: str
            file path to the config file.
        param: None, str 
            Default: None
            None: returns all config parameters as a dictionary.
            str: returns the parameter value of the keyword entered.
    '''
    assert type(config_dir) == str
    assert type(param) == None

    data = None
    with open(config_dir) as f:
        data = json.load(f)
    print(data)

if __name__ == "__main__":
    extract_config('./config.json')