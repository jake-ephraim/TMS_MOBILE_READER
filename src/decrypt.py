import json
from pathlib import Path


config_dir = "./config.json"
max_byte = 4 * 1024
file_id = 1000

example_dir = './data/test_file.tms'

def decryptFile(file_name: str) -> bool:
    '''
    Decrypts the '.tms' file format to its original format.

        file_name: name of the file to be decrypted.
    '''
    ## confirm file directory and name
    if Path(file_name).exists() is False:
        return False
    
    ## read config.json
    encryption_key = extract_config(config_dir, 'ENCRYPTION_KEY')
    print_data = extract_config(config_dir, 'PRINT')
    print_len = len(print_data)
    temp_folder = extract_config(config_dir, 'TEMP_FOLDER')
    
    ## read all data in the file
    if file_name == "":
    	return False
    with open(file_name, 'rb') as f:
        file = f.read()
        
        ## seek the inprint data
        start, end = -1, (-1*(print_len+1))
        while True:
            f1 = file[start:end:-1].decode('utf-8')[::-1]
            if f1 == print_data:
                break
            start -= 1
            end -= 1 

        ## slice out extension and inprint data (####### I ommited the last byte (starting from -2) incase of future bug)
        extension = file[-2:start:-1].decode('utf-8')[::-1]
        file = file[0:end+1]

        ## decrypt the file with the decryption key**
        if max_byte < len(file):
            decryptable = bytearray(file[: max_byte])
            non_decryptable = bytearray(file[max_byte:])
        else:
            decryptable = bytearray(file[:])
            non_decryptable = bytearray()

        for i in range(len(decryptable)):
            decryptable[i] = (decryptable[i] + encryption_key) % 256
        
        decryted_file = bytes(decryptable + non_decryptable)
    
    ## rewrite file
    writefile = Path(f'{temp_folder}/file{file_id}{extension}')
    with writefile.open('wb') as f:
        f.write(decryted_file)

def extract_config(config_dir: str, param=None):
    '''
        Collects all or some parameters from the config file.

        Dependencies: json and Pathlib.path

        config_dir: str
            file path to the config file.
        param: None, str 
            Default: None
            None: returns all config parameters as a dictionary.
            str: returns the parameter value of the keyword entered.
        return: dict, str or None.
    '''
    if Path(config_dir).exists() is False:
        return None
    with open(config_dir) as f:
        data = json.load(f)
    return data if param == None else data[param]

if __name__ == "__main__":
    decryptFile(example_dir)
