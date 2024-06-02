import os
import glob
import shutil

path = "../atm_forcing.datm7.uELM_NADaymet.1d.c231120"

# Check if the directory exists
if os.path.isdir(path):
    # If it exists, remove it
    shutil.rmtree(path)

# Create a new folder
os.makedirs(path)
# Change to the new directory
os.chdir(path)

# Get a list of all files in the input_data directory
files = glob.glob('../forcing/*')

# Loop through the files
for file in files:
    # Check if 'clmforc' is in the file name
    if 'clmforc' in file:
        # Split the file name on '_'
        parts = file.split('_')
        # Use the string after the '_' to create a soft link
        link_name = parts[1]

        command = 'ln -s '+ file + ' ' + link_name
        print(command)
        os.system(command)
        #os.exec(ln -s ../data/file link_name)
        #print("ln -s "+ "../data/"+ file + " " + link_name)
