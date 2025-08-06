#Compression and timstamp function from manifest
#Author: Fahad Rajper

import tarfile
import os
from datetime import datetime

def compress_from_manifest(manifest_file, output_dir):

    # Expand ~ if it's in the output path
    output_dir = os.path.expanduser(output_dir)

    # Check if output directory exists, create it if not
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Load file list from manifest
    if not os.path.isfile(manifest_file):
        print("Manifest file not found:", manifest_file)
        return

    with open(manifest_file, 'r') as mf:
        files = [line.strip() for line in mf if os.path.isfile(line.strip())]

    if not files:
        print("No valid files to compress.")
        return

    # Timestamp + full archive path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_{timestamp}.tar.gz"
    archive_name = os.path.join(output_dir, filename)  # maybe fixed


    with tarfile.open(archive_name, "w:gz") as tar:
        for file in files:
            tar.add(file, arcname=os.path.basename(file))
            print("Added:", file)

    print("Archive created:", archive_name)
