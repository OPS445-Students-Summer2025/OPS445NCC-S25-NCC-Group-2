#this function will compress and time stamp the current directory for the overall assignment which is backup and restore.
#Author: Fahad Rajper - Assignment 2


import os, zipfile, sys
from datetime import datetime

# Define a function to zip the folder
def zip_folder(folder):
    # Create a timestamp string for the zip file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Combine folder name with timestamp to name the zip file
    zip_name = folder + "_" + timestamp + ".zip"
    print("Creating zip:", zip_name)

    # Create the zip file in write mode ('w')
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        # Walk through the folder and all subfolders
        for root, _, files in os.walk(folder):
            for file in files:
                # Get the full path to the file
                path = os.path.join(root, file)

                # Get the path relative to the folder root (for inside zip)
                rel = os.path.relpath(path, folder)

                # Add the file to the zip archive
                zipf.write(path, rel)

    print("Done.")
    return zip_name  # Return the name of the zip file created

# This block runs only when script is run directly (not imported)
if __name__ == "__main__":
    # If no folder is provided, show usage and exit
    if len(sys.argv) < 2:
        print("Usage: python3 comp.py <folder_name>")
        sys.exit(1)

    # Get the folder name from the first argument
    folder = sys.argv[1]

    # Check if the folder exists
    if not os.path.isdir(folder):
        print("Error: Not a valid folder:", folder)
        sys.exit(1)

    # Call the function to zip the folder
    zip_folder(folder)

