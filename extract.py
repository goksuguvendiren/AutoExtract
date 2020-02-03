from os import listdir
from os.path import isfile, join
import subprocess
import os
import sys

def extract_submissions(folder_path):
    files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
    for file in files:
        print(file)
        index = file.find(".tar.Z")
        if index == -1:
            continue
        name = file[:index]
        pathname = os.getcwd() + "/" + name

        extract_student(file, pathname)


def extract_student(file, pathname):
    if not os.path.exists(path):
        print("Creating subfolder : " + pathname)
        os.mkdir(pathname)

    retcode = subprocess.call(["tar", "-xvzf", "../" + file, "-C", pathname])
    if retcode != 0:
        print("Could not extract " + file)

if __name__ == "__main__":
	if (sys.argv != 2):
		print ("Please give the path as command line argument")
		return
    extract_submissions(sys.argv[1])