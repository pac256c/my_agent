from functions.run_python_file import *

#test get_file_content
working_directory = "calculator"
files = ["main.py", "main.py", "tests.py", "../main.py", "nonexistent.py", "lorem.txt"]
args = [None, ["3 + 5"], None, None, None, None]
for i in range(len(files)):
    print(run_python_file(working_directory, files[i], args[i]))
    print("--------------------------------------------")