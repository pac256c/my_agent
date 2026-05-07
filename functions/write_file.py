import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try: 
        #check valid / absolute directory, target within working directory
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir

        #return string for errors 
        if not valid_target_file: return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file): return f'Error: Cannot write to "{file_path}" as it is a directory'

        #write the file
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        f = open(target_file, "w")
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing file {working_directory} + {file_path} - {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes/overwrites a file at path specified relative to working directory, using the content input as a string arg",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file we want to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String content that will be written to the file"
            ),
        },
    ),
)