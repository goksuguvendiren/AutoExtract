from os import listdir
from os.path import isfile, isdir, join
import subprocess
import os
import sys

def extract_submissions(folder_path):
    # files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
    if not os.path.exists(join(folder_path, "couldnt_extract")):
        os.mkdir(folder_path + "/couldnt_extract")
    if not os.path.exists(join(folder_path, "extracted")):
        os.mkdir(folder_path + "/extracted")
    if not os.path.exists(join(folder_path, "trash")):
        os.mkdir(folder_path + "/trash")
        
    folders = [folder for folder in listdir(folder_path) if isdir(join(folder_path, folder))]
    folders = [folder for folder in folders if folder.find("extract") == -1]
    folders = [folder for folder in folders if folder.find("trash") == -1]
    for folder in folders:
        print (folder)
        compressed_file = ""
        index_zip = -1
        for file in listdir(join(folder_path, folder)):
            # print (file)
            index_zip = file.find(".zip")
            if index_zip != -1:
                compressed_file = file
                break

        name = compressed_file[:index_zip]
        # print (name)
        output_location = join(join(folder_path, "extracted"), name)
        # print (pathname)

        if index_zip == -1:
            #means that couldn't extract what's inside the folder
            source_folder = join(folder_path, folder)
            destin_folder = join(join(folder_path, "couldnt_extract"), folder)
            print ("couldn't extract submission: "  + source_folder)
            print ("moving to location: "  + destin_folder)
            os.rename(source_folder, destin_folder)
        else:
            extract_student_zip(join(join(folder_path, folder), compressed_file), output_location)
            source_folder = join(folder_path, folder)
            destin_folder = join(join(folder_path, "trash"), folder)
            # print ("extracted submission: "  + source_folder)
            # print ("moving to location: "  + destin_folder)
            os.rename(source_folder, destin_folder)


def extract_student_tar_gz(file, pathname):
    if not os.path.exists(path):
        print("Creating subfolder : " + pathname)
        os.mkdir(pathname)

    retcode = subprocess.call(["tar", "-xvzf", "../" + file, "-C", pathname])
    if retcode != 0:
        print("Could not extract " + file)

def extract_student_zip(file, pathname):
    if not os.path.exists(pathname):
        print("Creating subfolder : " + pathname)
        os.mkdir(pathname)

    print ("Extracting:")
    print (join(pathname, file))

    retcode = subprocess.call(["unzip", file, "-d", pathname])
    if retcode != 0:
        print("Could not extract " + file)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Please give the path as command line argument")
        print("Exiting...")
        exit(0)
    folder_path = sys.argv[1]
    extract_submissions(folder_path)