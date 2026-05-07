import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        #check valid / absolute directory, target within working directory
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir

        #return string for errors 
        if not valid_target_file: return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file): return f'Error: File not found or is not a regular file: "{file_path}"'

        #read the file
        f = open(target_file, "r")
        content = f.read(MAX_CHARS)
        if f.read(1): content += f'\n[...File "{file_path} truncated at {MAX_CHARS} characters]'
        return content

    except Exception as e:
        return f"Error: reading file {working_directory} + {file_path} - {e}"