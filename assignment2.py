# Restore function updated after team review

import os
import tarfile
import argparse

def restore_backup(backup_file, restore_path):
    if not os.path.isfile(backup_file):
        print(f"[ERROR] Backup file '{backup_file}' does not exist.")
        return

    if not os.path.exists(restore_path):
        print(f"[INFO] Creating restore directory: {restore_path}")
        os.makedirs(restore_path)

    try:
        with tarfile.open(backup_file, "r:gz") as tar:
            tar.extractall(path=restore_path)
        print(f"[SUCCESS] Backup restored to: {restore_path}")
    except tarfile.TarError as e:
        print(f"[ERROR] Restore failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Backup and Restore Tool")
    parser.add_argument('--restore', help='Path to .tar.gz backup file')
    parser.add_argument('--destination', help='Restore location')
    args = parser.parse_args()

    if args.restore and args.destination:
        restore_backup(args.restore, args.destination)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
