from os import listdir
from os.path import isfile, join, isdir
import subprocess
import sys
import os
import fnmatch
from pathlib import Path
import json

from colorama import Fore, Back, Style

path = os.getcwd()

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def run_submission(source_path, compiled_path):
	# go to the subdirectory of the submission
	os.chdir(source_path)
	print(source_path)

	submission_path = source_path.parent
	if str(source_path.parent).endswith("compiled"):
		submission_path = source_path
	buildpath = source_path / "goksubuild"

	print ("The source code is in: " + str(source_path))
	print ("Compiled the code into: " + str(buildpath))
	print ("Whole submission is in: " + str(submission_path))
	# if ~buildpath.resolve().exists():
	# # 	buildpath.mkdir(mode=0o777, parents=True, exist_ok=True)
	# 	print("The build folder: goksubuild doesn't exist, continuing!")
	# 	return 

	os.chdir(buildpath)
	
	# run the submission
	cmake_retcode = subprocess.call(["ls"])

	executable = find("Rasterizer", buildpath)
	if (len(executable) == 0):
		print ("Executable doesn't exist in: " + str(buildpath))
		return

	retcode = subprocess.call(["./Rasterizer", "-r", "0", "output0.png"])
	retcode = subprocess.call(["./Rasterizer", "-r", "10", "output10.png"])
	retcode = subprocess.call(["./Rasterizer", "-r", "20", "output20.png"])

	if (retcode != 0):
		print ("Couldn't run the code!")

	grade = int(input("Final Grade: "))

	return grade

def iterate_through_folders(folder_path, compiled_path):
	# folder_path => the folder that contains all the extracted submissions
	
	dict = {"goksu": 100}

	folders = [folder for folder in folder_path.iterdir() if (folder_path / folder).is_dir()]
	for folder in folders:
		# print ("folder: " + str(folder))
		# each folder is a student's assignment

		# print folder
		cmake_path = find("CMakeLists*", str(folder))

		if len(cmake_path) != 1:
			print ("MULTIPLE OR ZERO CMAKELISTS SOMEHOW!")
			continue
		else:
			readme_path = find("README*", str(folder))
			if (len(readme_path) != 1):
				print ("No README file!")
				continue
			else:
				print ("FOUND README file!")
				print (folder.name)

		source_path = Path(cmake_path[0])

		grade = run_submission(source_path.parent, compiled_path)
		dict[folder.name] = grade

	print (dict)
	grade_file = compiled_path / "grades.json"
	with open(grade_file, 'w') as fp:
		json.dump(dict, fp)

	print("Saved the grades file into: " + str(grade_file))

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