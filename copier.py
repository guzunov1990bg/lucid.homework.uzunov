from genericpath import exists
import requests
import shutil
import urllib
import urllib.request
import argparse
import json
import time
import os
import subprocess


desc = 'Welcome to the copier script for the LucidLink Technical Support Engineer Level 3 practical assignment. You need to parse a file and destination for the copy process to start.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("file", type=str)
parser.add_argument("destination", type=str)

args = parser.parse_args()


def copy_this_file(file, destination):
    """
    This function is responsible for the copying of the file, various checks like:
    - Check if the file already exists.
    - Check if we have a valid mount/destination.
    - Check if the destination exsts | if not will be created.
    - Checking if we have 0 dirtyBytes.
    - Sending the empty PUT request.
    """
    try:
        check_valid_mount(destination) # Checking if we have a valid destination served to the script file.
        check_if_destination_exist(destination) # Checking if we have the destination in the lucid volume, if we don't have a folder for example it will be created.
        check_if_file_exists(destination, file) # Checking if the file exists, if it does there will be a message that the file will be overwritten.
        shutil.copyfile(file, destination + "/" + file) # We are using the built in shutil function to initiate the copy of files.
        print("Initiating copying of file {} to {}".format(file, destination))
        while get_dirtyBytes() != 0: # While we're copying the files we're checking for the value of the dityBytes. If it's not 0, we're printing copying.
            print('Copying...')
            time.sleep(2) # 2 seconds sleep time to avoind too much spam.
            if get_dirtyBytes() == 0: # Once the dirtyBites go back to zero we print the line below.
                print('Copy complete dirtyBites field is equal to 0.')
                if send_empty_put() == 200: # We're checking if we have return code 200 when we send the empty put request and print the line below.
                    print("Code 200 returned, file index changes have been synchronized with the cloud.")

    except ValueError: # If something goes wrong with the block below the script will raise an error and quit.
                print("Something went wrong while trying to copy files to Lucid.")
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
        print("Copy destination is not a valid Lucid link.")
        exit()
    
def check_if_destination_exist(destination):
    """
    This function checks if the destination path exist and if it doesn't will create the directory.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

def check_if_file_exists(destination, file):
    """
    This function checks if file exists and it will display a warning that the file can be overwritten.
    """
    if exists(destination + "/" + file):
        print('Warning file already exists, it will be overwritten!')
        input("Press Enter to continue or ctrl+c to stop.")
    



if __name__ == '__main__':
    print("############################")
    print("        STARTING WORK    ")
    print("############################")
    copy_this_file(args.file, args.destination)
    print("############################")
    print("         END WORK    ")
    print("############################")
