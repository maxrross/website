import pymongo
import os
import sys
import certifi
from getData import get_data
from user import username, password
import json
import fnmatch


def create_user_file():
    # create the file
    username = input("Enter username: ")
    password = input("Enter password: ")
    name_of_user = input("Enter name of user: ")
    with open("user.py", "w") as file:
        file.write(
            '# this file stores usernames and passwords for the database\nusername="{username}"\npassword="{password}"\nname_of_user="{name_of_user}"'.format(
                username=username, password=password, name_of_user=name_of_user
            )
        )


# if not os.path.exists("user.py"):
#  create_user_file()
from user import username, password, name_of_user


client = pymongo.MongoClient(
    "mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/test".format(
        username=username, password=password
    ),
    tlsCAFile=certifi.where(),
)
db = client.Flakes
clt_name = (
    input("Please select collection [1]:DGQD, [2]:FEXGQD, [3]:LIG, input number: ")
    or "Unsorted"
)
collection = db[clt_name]

# Define the root directory to search for .log files
root_dir = "./"
logfiles = []
# Loop through all the subdirectories and files in the root directory
for root, dirnames, filenames in os.walk(root_dir):
    # Loop through all the filenames in the current directory
    for filename in filenames:
        # Check if the filename ends with .log
        if fnmatch.fnmatch(filename, "*.log"):
            # Print the absolute path of the file
            file_path = os.path.abspath(os.path.join(root, filename))
            logfiles.append(file_path)

molecules = get_data(logfiles)
uploader = input("Please input the uploader name/alias: ") or "MJ"
for mol in molecules:
    mol = mol.__dict__
    if mol["status"] != "Error":
        mol["identifier"] = f"{mol['name']}_{mol['basis_sets']}_{mol['functional']}"
        mol["uploader"] = uploader

    ret_val = collection.insert_one(mol)
    if ret_val.acknowledged:
        print("Successfully inserted molecule: {name}".format(name=mol["name"]))
