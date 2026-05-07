from functions.get_file_content import *

#test get_file_content
working_directory = "calculator"
files = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
for file in files:
    print(get_file_content(working_directory, file))
    print("--------------------------------------------")