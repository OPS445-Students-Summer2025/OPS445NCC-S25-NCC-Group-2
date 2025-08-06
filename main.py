#!/usr/bin/env python3

import os
import datetime
import sys
from argparser import parse_args
from backup import full_backup, incremental_backup, file_manifest, manifest_timestamper
from restore_backup import restore_backup
from compression import compress_files
from logging import log_operation

def main():
    args = parse_args()
    mode = args.mode.lower()
    source = args.source
    destination = args.destination

    if mode == "backup":
        # Determine backup type: full or incremental
        if args.timestamp:
            try:
                last_backup_time = datetime.datetime.strptime(args.timestamp, "%Y-%m-%d_%H:%M:%S")
                files = incremental_backup(source, last_backup_time)
                backup_type = "incremental"
            except ValueError:
                print("Invalid timestamp format. Use YYYY-MM-DD_HH:MM:SS")
                sys.exit(1)
        else:
            files = full_backup(source)
            backup_type = "full"

        # Generate manifest and proceed to compression
        manifest_path = manifest_timestamper(backup_type)
        manifest_written = file_manifest(files, manifest_path)

        if not manifest_written:
            print("No files to back up. Exiting.")
            sys.exit(0)

        if not os.path.exists(destination):
            print(f"Creating backup destination directory: {destination}")
            os.makedirs(destination)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        archive_name = f"backup_{backup_type}_{timestamp}.tar.gz"
        output_path = os.path.join(destination, archive_name)

        compressed = compress_files(manifest_path, output_path)
        if compressed:
            log_operation("backup", source, output_path)

    elif mode == "restore":
        if not os.path.isfile(source):
            print(f"Backup archive not found: {source}")
            sys.exit(1)

        if not os.path.isdir(destination):
            print(f"Destination does not exist. Creating: {destination}")
            os.makedirs(destination)

        restore_backup(source, destination)
        log_operation("restore", source, destination)
        sys.exit(0)

if __name__ == "__main__":
    main()