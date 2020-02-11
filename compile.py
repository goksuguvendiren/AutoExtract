from os import listdir
from os.path import isfile, join, isdir
import subprocess
import sys
import os
import fnmatch
from pathlib import Path

from colorama import Fore, Back, Style

path = os.getcwd()

def compile_student(source_path, compiled_path):
	# go to the subdirectory of the submission
	os.chdir(source_path)
	print(source_path)

	source_path = Path(source_path)
	submission_path = source_path.parent
	if str(source_path.parent).endswith("extracted"):
		submission_path = source_path
	buildpath = source_path.resolve() / "goksubuild"
	print ("The source code is in: " + str(source_path))
	print ("Compiled the code into: " + str(buildpath))
	print ("Whole submission is in: " + str(submission_path))
	if ~buildpath.exists():
		buildpath.mkdir(mode=0o777, parents=True, exist_ok=True)
		print("created the build folder: goksubuild")

	os.chdir(buildpath)
	
	# compile the code
	cmake_retcode = subprocess.call(["cmake", ".."])
	if (cmake_retcode != 0):
		print("Could not compile " + str(source_path))
	else:
		make_retcode = subprocess.call(["make", "-j12"])
		if (make_retcode != 0):
			print("Could not compile " + str(source_path))
		else:
			print("Compiled successfully: " + str(source_path))
		# copy the folder into the "compiled" folder
		# print "Compiled folder is at : " + join(path, "compiled")
		# subprocess.call(["mv", fullpath, join(path, "compiled")])
			print ("COMPILED FOLDER: " + str(compiled_path))
			print ("SUBMISSION FOLDER: " + str(submission_path))
			subprocess.call(["mv", submission_path, str(compiled_path)])

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def iterate_through_folders(folder_path, compiled_path):
	# folder_path => the folder that contains all the extracted submissions
	
	folders = [folder for folder in folder_path.iterdir() if (folder_path / folder).is_dir()]
	for folder in folders:
		print (folder)
		# each folder is a student's assignment

		fullpath = folder_path / folder
		print (fullpath)
		# print folder
		cmake_path = find("CMakeLists*", str(fullpath))

		if len(cmake_path) != 1:
			print ("MULTIPLE OR ZERO CMAKELISTS SOMEHOW!")
			continue

		source_path = Path(cmake_path[0])

		compile_student(str(source_path.parent), compiled_path)

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print("Please give the path as command line argument")
		print("Exiting...")
		exit(0)

	folder_path = Path(sys.argv[1])
	compiled_path = folder_path.parent / "compiled"
	if ~compiled_path.exists():
		compiled_path.mkdir(mode=0o777, parents=True, exist_ok=True)
		print("created the compiled folder: " + str(compiled_path))

	iterate_through_folders(folder_path.resolve(), compiled_path.resolve())