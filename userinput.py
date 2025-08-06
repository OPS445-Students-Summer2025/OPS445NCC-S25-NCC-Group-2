#!/usr/bin/env python3
'''
OPS445 Assignment 2 - Group 2 
by: Pablo Gomez  
Semester: Summer 2025  

Description:  
the code handles user input from the command line using argparse.  
it collects required options as backup or restore,source and destination paths,directories to exclude and timestamp  
'''
import argparse
import sys

def parse_args():
    user_input = argparse.ArgumentParser()

    user_input.add_argument("--mode", required=True)
    user_input.add_argument("--source", required=True)
    user_input.add_argument("--destination", required=True)
    user_input.add_argument("--exclude", nargs='*')
    user_input.add_argument("--timestamp")

    end = user_input.parse_args()

    if end.mode not in ["backup", "restore"]:
        print("Error: --mode must be backup or restore")
        print("Example: --mode backup --source /folder --destination /backup")
        sys.exit(1)

    return end

if __name__ == "__main__":
    end = parse_args()
    print("Mode:", end.mode)
    print("Source:", end.source)
    print("Destination:", end.destination)
    print("Exclude:", end.exclude)
    print("Timestamp:", end.timestamp)
