#!/usr/bin/env python3

import datetime
import os

'''
OPS445 Assignment 2 - Group 2
Program: assignment2.py: backup.py
Author: Ronald Lu
Semester: Summer 2025
Description: 
Scans specified directories to identify files for full or incremental backups.
Writes a list of file paths to a manifest file for later compression.
'''

def excluded_files(path):
    """Checks for any trash files that exist within the target path"""
    trash_files = ["__pycache__", ".tmp", "cache", ".temp", ".log"] # unnecessary file types that don't need to be included in backups
    for keyword in trash_files: # check if path contains unwanted files
        if keyword in path:
            return True
    return False

def full_backup(source_dir): 
    filepath = []
    # source: https://docs.python.org/3/library/os.html
    for root, _, files in os.walk(source_dir): # excluded dirs, not using it in this case
        for name in files:
            path = os.path.join(root, name)
            if not excluded_files(path):
                filepath.append(path)
    return filepath

def incremental_backup():
    pass


def file_manifest(file_list, manifest_path):
    """Writes the list of files to be used for compression, overwrites existing manifests""" 
    try:
        with open(manifest_path, 'w') as manifest_file:
            for filepath in file_list:
                manifest_file.write(filepath + "\n")
        print(f"Manifest file written to: {manifest_path}")
    except Exception as e:
        print(f"Failed to write manifest: {e}")
    
# testing functions, remove when complete
if __name__ == "__main__":
    source_dir = "test_dir"
    manifest_path = "backup_manifest.txt"

    backup_test = full_backup(source_dir)
    file_manifest(backup_test, manifest_path)

    print("something happened here!")
    with open("backup_manifest.txt", "r") as file:
        print(f"Filtered list: \n{file.read()}")

