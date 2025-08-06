import tarfile
import os
from datetime import datetime

def compress_from_manifest(manifest_file):
    """
    Reads a manifest file and compresses the listed files into a .tar.gz archive.
    The output archive will have a timestamp in its name.
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

    # Create a timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.tar.gz"

    # Create the .tar.gz archive
    with tarfile.open(archive_name, "w:gz") as tar:
        for file in files:
            # Add each file using only its filename (not full path)
            tar.add(file, arcname=os.path.basename(file))
            print("Added:", file)

    print("Archive created:", archive_name)
