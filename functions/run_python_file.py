import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try: 
        #check valid / absolute directory, target within working directory
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir

        #return string for errors 
        if not valid_target_file: return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file): return f'Error: "{file_path}" does not exist or is not a regular file: '
        if not target_file[-3:] == ".py": return f'Error: "{file_path}" is not a Python file'

        #run the python file
        command = ["python", target_file]
        if args is not None: command += args
        completed_proc = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output_str = ""
        if completed_proc.returncode != 0: output_str += f"Process exited with code {completed_proc.returncode}\n"
        if completed_proc.stdout is None and completed_proc.stderr is None: output_str += "No output produced\n"
        else:
            if completed_proc.stdout is not None: output_str += f"STDOUT: {completed_proc.stdout}"
            if completed_proc.stderr is not None: output_str += f"STDERR: {completed_proc.stderr}"
        return output_str

    except Exception as e:
        return f"Error: run_python_file {working_directory} + {file_path} error - {e}"