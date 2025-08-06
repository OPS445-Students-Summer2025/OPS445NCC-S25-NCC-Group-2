
#!/usr/bin/env python3

import os
import datetime
import datetime
import os

def excluded_files(path):
    """Checks for any trash files that exist within the target path"""
    trash_files = ["__pycache__", ".tmp", "cache", ".temp", ".log"] # unnecessary file types that don't need to be included in backups
    for keyword in trash_files: # check if path contains unwanted files
        if keyword in path:
            return True
    return False


def full_backup(source_dir): 
    """Full backup: backs up all items within a directory"""
    filepath = []
    # source: https://docs.python.org/3/library/os.html
    for root, _, files in os.walk(source_dir): # excluded dirs, not using it in this case
        for name in files:
            path = os.path.join(root, name)
            if not excluded_files(path): # skip trash files
                filepath.append(path)
    return filepath


def incremental_backup(source_dir, last_backuptime):
    """Incremental backup: backs up items"""
    modified_files = []
    for root, _, files in os.walk(source_dir):
        for name in files:
            path = os.path.join(root, name)
            try:
                modif_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)) 
                if modif_time > last_backuptime and not excluded_files(path): # compares timestamp of path to last completed backup and skips trash
                    modified_files.append(path)
            except Exception as e:
                print(f"Could not read file: {path}, reason: {e}")
    return modified_files


def file_manifest(file_list, manifest_path):
    """Writes the list of files to be used for compression""" 
    if not file_list:
        print(f"No changes detected, skipping incremental manifest creation.")
        return False
    try:
        with open(manifest_path, 'w') as manifest_file: # creates a manifest containing the files to be packaged by the compression function
            for filepath in file_list:
                manifest_file.write(filepath + "\n")
        print(f"Manifest file sucessfully written to: {manifest_path}")
        return True
    except Exception as e:
        print(f"Failed to write manifest: {e}")

def manifest_timestamper(backup_type, manifest_dir=os.path.expanduser("~/manifests")):
    """Applies timestamps to all manifests created. Manifests are stored in ~/manifests by default."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # source: https://docs.python.org/3.6/library/datetime.html
    os.makedirs(manifest_dir, exist_ok=True) # create manifest directory if it doesn't exist, default location ~/manifests
    return os.path.join(manifest_dir, f"backup_{backup_type}_{timestamp}.manifest")

# testing functions, remove when complete
if __name__ == "__main__":
    """Assuming that a test directory is present in pwd"""
    source_dir = "test_dir"
    manifest_path = os.path.expanduser("~/manifests")

    # full backup test
    fbackup_test = full_backup(source_dir)
    ffile_manifest_path = manifest_timestamper("full", manifest_path)
    file_manifest(fbackup_test, ffile_manifest_path)

    # incremental backup on file changed in the past minute (change something in test directory first)
    last_backup = datetime.datetime.now() - datetime.timedelta(minutes=1) # looks for changes to source directory files within past minute (when in production, make a persistent comparison)
    inc_files = incremental_backup(source_dir, last_backup)
    inc_manifest_path = manifest_timestamper("inc", manifest_path)
    file_manifest(inc_files, inc_manifest_path)

