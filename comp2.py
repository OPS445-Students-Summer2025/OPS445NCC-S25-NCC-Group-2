#Compression and timstamp function from manifest
#Author: Fahad Rajper

import tarfile
import os
from datetime import datetime

def compress_from_manifest(manifest_file, output_dir):
    """
    Reads a manifest file and compresses the listed files into a .tar.gz archive.
    The output archive will be saved to the specified directory with a timestamp in its name.
    """

    # Check if the manifest file exists
    if not os.path.isfile(manifest_file):
        print("Manifest file not found:", manifest_file)
        return

    # Read file paths from the manifest
    with open(manifest_file, 'r') as mf:
        files = [line.strip() for line in mf if os.path.isfile(line.strip())]

    # If no valid files were found, exit
    if not files:
        print("No valid files to compress.")
        return

    # Create a timestamped filename in the output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    archive_name = os.path.join(output_dir, f"backup_{timestamp}.tar.gz")

    # Create the .tar.gz archive
    with tarfile.open(archive_name, "w:gz") as tar:
        for file in files:
            tar.add(file, arcname=os.path.basename(file))
            print("Added:", file)

    print("Archive created:", archive_name)
