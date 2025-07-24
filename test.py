# from functions.get_file_content import get_file_content
from functions.get_file_content import get_file_content
from functions.write_file import write_file
import os


# get_files_info(os.getcwd(), "calculator/pkg")
# file = get_file_content(os.getcwd(), "calculator/lorem.txt")
#
# print(file)
#

write_file(os.getcwd(), "test.txt", "Hello World")
file = get_file_content(os.getcwd(), "test.txt")
print(file)
