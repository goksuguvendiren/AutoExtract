from os import listdir
from os.path import isfile, join, isdir
import subprocess
import os

path = os.getcwd()

def compile_student(fullpath):
	# go to the subdirectory of the submission
	os.chdir(fullpath)

	# compile the code
	retcode = subprocess.call(["make"]);
	if (retcode != 0):
		print "Could not compile " + fullpath
	else:
		# copy the folder into the "compiled" folder
		# print "Compiled folder is at : " + join(path, "compiled")
		subprocess.call(["mv", fullpath, join(path, "compiled")])	


path = os.getcwd() 
files = [file for file in listdir(path) if isdir(join(path, file))]

for file in files:
	print file
	fullpath = join(path, file)

	compile_student(fullpath)
