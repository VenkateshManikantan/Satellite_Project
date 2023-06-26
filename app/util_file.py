import os 
import pandas as pd 
import numpy as np



def get_dir(path_to_folder):
    """Function: Get all paths and name of files.

    `Function to get all names and dir roots of all files'

    Parameters
    ----------
    path_to_folder : string 
        path to the targeted folder 
    Returns
    -------
    output_1: List
         dir full list
    output_2: List
         name full list 
    """
    file_name = []
    dir_name  = []
    for root, dirs, files in os.walk(path_to_folder):
        for file in files:
            if file.endswith('.jpg'):
                file_name.append(file)
                dir_name.append(os.path.join(root,file))

    file_name = np.array(file_name)
    dir_name = np.array(dir_name)
    return file_name , dir_name

def find_between( s, first, last ):
    """Function: Get all paths and name of files.

    `Function to get all names and dir roots of all files'

    Parameters
    ----------
    s : string 
        Path to the targeted folder 
    first: string 
        The starting char
    last: string
        The ending char
    Returns
    -------
    returns 
    """
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""