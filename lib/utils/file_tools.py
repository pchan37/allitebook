import os
import errno

def assure_directory_path_exists(directory_path):
    '''
    Assure that the given path exists

    Attempt to create the directories on the given path and ignore the error
    if the directories already exist.

    Args:
        directory_path (str): the directory path we want to assure exist

    Returns:

    Raises:
        OSError: Exception preventing the creation of directory ignoring the error
            if the directories already exist
    '''
    try:
        os.makedirs(directory_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
