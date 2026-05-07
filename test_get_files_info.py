from functions.get_files_info import *

#test get_files_info
working_directory = "calculator"
directories = [".", "pkg", "/bin", "../"]
for directory in directories:
    print(get_files_info(working_directory, directory))
    print("--------------------------------------------")