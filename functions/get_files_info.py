import os

def get_files_info(working_directory, directory="."):
    #check valid / absolute directory, target within working directory
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir

    #list contents of directory, error 
    contents = f"Result for {"current" if directory == "." else directory} directory:\n"
    if not valid_target_dir: return contents + f'    Error: Cannot list "{target_dir}" as it is outside the permitted working directory\n'
    if not os.path.isdir(target_dir): return contents + f'    Error: "{target_dir}" is not a directory\n'

    #list files/directories in the directory specified
    for item in os.listdir(target_dir):
        try:
            file_size = os.path.getsize(target_dir + "/" + item)
            is_dir = os.path.isdir(target_dir + "/" + item)
            contents = "".join([contents, f"  - {item}: file_size={file_size} bytes, is_dir={is_dir}\n"])
        except OSError as e:
            return contents + f"    Error: hit os issue {e}"
    return contents
        