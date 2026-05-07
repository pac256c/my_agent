from functions.write_file import *

#test get_file_content
working_directory = "calculator"
files = ["lorem.txt", "pkg/morelorem.txt", "/tmp/temp.txt"]
text = ["wait, this isn't lorem ipsum", "lorem ipsum dolor sit amet", "this should not be allowed"]
for i in range(len(files)):
    print(write_file(working_directory, files[i], text[i]))
    print("--------------------------------------------")