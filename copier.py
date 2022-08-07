from genericpath import exists
import requests
import shutil
from distutils.dir_util import copy_tree
import urllib
import urllib.request
import argparse
import json
import time
import os
import subprocess


desc = 'Welcome to the copier script for the LucidLink Technical Support Engineer Level 3 practical assignment. You need to parse a file and destination for the copy process to start.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("object", type=str, help='specify a object to copy')
parser.add_argument("destination", type=str, help='specify a destination to copy to')

args = parser.parse_args()


def main(object, destination):

    """
    This function is responsible for the copying of the Object, various checks like:
    - Check if the Folder/File already exists.
    - Check if we have a valid mount/destination.
    - Check if the destination exists | if not will be created.
    - Checking if we have 0 dirtyBytes.
    - Sending the empty PUT request.
    """

    try:
        check_if_object_to_copy_exists(object) # Check if the object we want to copy exists at source.
        check_valid_mount(destination) # Checking if we have a valid destination served to the script.
        if os.path.isdir(object): # If we copy a directory we use this portion of the script.
            converted_objectname = object.split("/")[-2] # Splitting up the object so we can only get the last folder we would like to copy.
            check_if_object_exists_on_volume(converted_objectname, destination) # Checking if the object exists on the Lucid volume, if it does there will be a message that the object will be overwritten.
            check_if_destination_exist(destination) # Checking if we have the destination on the lucid volume, if we don't have a folder for example it will be created.
            copy_tree(object, destination + "/" + object.split("/")[-2]) # Copying of the folder.
            print("Initiating copying folder {} to {}".format(object, destination))
            while get_dirtyBytes() != 0: # While we're copying the files we're checking for the value of the dityBytes. If it's not 0, we're printing copying.
                print('Copying...')
                time.sleep(2) # 2 seconds sleep time to avoind too much spam.
                if get_dirtyBytes() == 0: # Once the dirtyBites go back to zero we print the line below.
                    print('Copy complete dirtyBites field is equal to 0.')
                    if send_empty_put() == 200: # We're checking if we have return code 200 when we send the empty put request and print the line below.
                        print("Code 200 returned, file index changes have been synchronized with the cloud.")

        elif os.path.isfile(object): # If we copy a file we use this portion of the script.
            converted_objectname = object.split("/")[-1] # Splitting up the object so we can only get the file want to copy.
            check_if_object_exists_on_volume(converted_objectname, destination) # Checking if the object exists on the Lucid volume, if it does there will be a message that the file will be overwritten.
            check_if_destination_exist(destination) # Checking if we have the destination on the lucid volume, if we don't have a folder for example it will be created.
            shutil.copyfile(object, destination + "/" + converted_objectname) # We are using the built in shutil function to initiate the copy of files.
            print("Initiating copying of file {} to {}".format(converted_objectname, destination))
            while get_dirtyBytes() != 0: # While we're copying the files we're checking for the value of the dityBytes. If it's not 0, we're printing copying.
                print('Copying...')
                time.sleep(2) # 2 seconds sleep time to avoind too much spam.
                if get_dirtyBytes() == 0: # Once the dirtyBites go back to zero we print the line below.
                    print('Copy complete dirtyBites field is equal to 0.')
                    if send_empty_put() == 200: # We're checking if we have return code 200 when we send the empty put request and print the line below.
                        print("Code 200 returned, file index changes have been synchronized with the cloud.")

    except ValueError: # If something goes wrong with the block below the script will raise an error and quit.
                print("Something went wrong while trying to copy Object to Lucid.")
                exit()
    

def send_empty_put():
    """
    This function is responsible for sending the empty put request after the copy is complete and making sure that the file index changes have also been synchronized with the cloud.
    """
    json = {}
    response = requests.put("http://localhost:7778/app/sync", json=json)
    return response.status_code

def get_dirtyBytes():
    """
    This function is responsible for getting the dirtyBytes.
    """
    url ="http://localhost:7778/cache/info"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    values = json.loads(data)
    return values['dirtyBytes']

def check_valid_mount(destination):
    check = subprocess.getstatusoutput(f"lucid status | grep 'Mount point'")
    if check[1].split(":")[1].strip() in destination :
        print('Copy destination is valid!')
    else:
        print("Copy destination is not a valid Lucid link. Exiting the script!")
        exit()
    
def check_if_destination_exist(destination):
    """
    This function checks if the destination path exist and if it doesn't it will create the directory.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

def check_if_object_exists_on_volume(object, destination):
    """
    This function checks if object exists and it will display a warning that the object can be overwritten.
    """
    if exists(destination + "/" + object):
        print('Warning object already exists, it will be overwritten!')
        input("Press Enter to continue or ctrl+c to stop.")
    
def check_if_object_to_copy_exists(object):
    if exists(object):
        print("Object to copy is valid!")
    else:
        print("Object {} is not valid and cannot be copied. Exiting script!".format(object))
        exit()


if __name__ == '__main__':
    print("############################")
    print("        STARTING WORK    ")
    print("############################")
    main(args.object, args.destination)
    print("############################")
    print("         END WORK    ")
    print("############################")
