import os

def get_files_info(working_directory, directory="."):
    try:
        #check valid / absolute directory, target within working directory
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir

        #list contents of directory, error 
        if not valid_target_dir: return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory\n'
        if not os.path.isdir(target_dir): return f'Error: "{target_dir}" is not a directory\n'

        #list files/directories in the directory specified
        contents = []
        for item in os.listdir(target_dir):
            file_size = os.path.getsize(os.path.join(target_dir,item))
            is_dir = os.path.isdir(os.path.join(target_dir,item))
            contents.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n")
        return "\n".join(contents)

    except Exception as e:
        return f"Error: listing files - {e}"