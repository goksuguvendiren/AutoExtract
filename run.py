from os import listdir
from os.path import isfile, join, isdir
from threading import Timer
import subprocess
import os
import ntpath
import time
import signal

def input_file_names(full_input_path):
	print full_input_path
	return [join(full_input_path, file) for file in listdir(full_input_path) if isfile(join(full_input_path, file))]

def execute_student(student_folder, input_files):
	build_path = join(student_folder, "build")
	if not os.path.exists(build_path):
		os.mkdir(build_path)

	output_path = join(build_path, "outputs")
	if not os.path.exists(output_path):
		os.mkdir(output_path)

	executable_path = join(student_folder, "prog2")

	if not os.path.exists(executable_path):
		print student_folder + " does not have the executable prog2"
		return

	for basic in input_files:
		print basic
		_, input_name = ntpath.split(basic)
		output_file = join(output_path, input_name)

		inp = open(basic)
		out = open(output_file, "w")

		# command = executable_path + " < " + basic + " > " + output_file
		command = [executable_path]
		proc = subprocess.Popen(command, stdin=inp, stdout=out, stderr=out)
		timer = Timer(5, proc.kill)
		try:
			timer.start()
			stdout, stderr = proc.communicate()
		finally:
			timer.cancel()
		# print command
		# retcode = os.system(command)
		# if (retcode != 0):
			# print "Could not run the command : " + fullpath


class Timeout(Exception):
	pass

def handler(signum, frame):
	print "Signam handler called with signal : " + signum
	raise Timeout

def main():
	#..../prog1/evaluation/
	script_path = os.getcwd()

	#..../prog1/evaluation/compiled
	compiled_path = join(script_path, "compiled")
	#..../prog1/evaluation/compiled/studentX/
	student_folders = [join(compiled_path, file) for file in listdir(compiled_path) if isdir(join(compiled_path, file))]

	input_folder = join(script_path, "inputs/")
	input_files = input_file_names(input_folder)

	# print basic_input_files
	# print student_folders[0]
	# execute_student(briankim, basic_input_files, advcd_input_files)
	for student in student_folders:
		print student
		execute_student(student, input_files)

if __name__ == "__main__":
	main()
