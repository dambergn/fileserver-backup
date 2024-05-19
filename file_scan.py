#!/usr/bin/python3
import os
import sys
import time
import json
import subprocess
import argparse

# Dependencies
#sudo apt-get update
#sudo apt-get install nfs-common

def ensure_root():
    """Ensure script is being run as root."""
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def mount_nfs(server, remote_dir, local_mount):
    # Check if local mount point exists. If not, create it.
    if not os.path.exists(local_mount):
        os.makedirs(local_mount)
    
    cmd = f"sudo mount -t nfs {server}:{remote_dir} {local_mount}"
    proc = subprocess.run(['bash','-c', cmd])
    
    if proc.returncode != 0:
        raise Exception(f'Failed to run command {cmd}. Error code: {proc.returncode}')
    
def unmount_nfs(local_mount):
    """Unmount an NFS share."""
    cmd = f"sudo umount {local_mount}"
    proc = subprocess.run(['bash','-c', cmd])
    
    if proc.returncode != 0:
        raise Exception(f'Failed to run command {cmd}. Error code: {proc.returncode}')

def get_file_info(directory):
    files = []
    total_size = 0
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            size = os.path.getsize(filepath)

            info = {
                'filename': filename,
                'relative_path': os.path.relpath(filepath, directory),
                'size': size,
                'last_modified': time.ctime(os.path.getmtime(filepath))
            }

            files.append(info)
            total_size += size

    return {'mount_location': f'{server}:{remote_dir}', 'number_of_files': len(files), 
        'total_size': total_size, 'files': files}

def get_media_file_info(directory):
    folders = []
    for root, dirs, filenames in os.walk(directory):
        if not dirs and not filenames:
            continue

        foldername = os.path.basename(root)
        relative_path = os.path.relpath(root, directory)
        size = 0
        files = []

        for filename in filenames:
            filepath = os.path.join(root, filename)
            file_size = os.path.getsize(filepath)

            info = {
                'filename': filename,
                'relative_path': os.path.relpath(filepath, directory),
                'size': file_size,
                'last_modified': time.ctime(os.path.getmtime(filepath))
            }

            size += file_size
            files.append(info)

        folder_info = {
            'foldername': foldername,
            'relative_path': relative_path,
            'size': size,
            'files': files
        }
        folders.append(folder_info)

    return {'mount_location': f'{server}:{remote_dir}', 'number_of_folders': len(folders), 
         'total_size': sum([folder['size'] for folder in folders]), 'folders': folders}

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
if  __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action='store_true')   # If -m flag is present, use get_media_ file_ info function
    args, unknown_args = parser.parse_known_args()   # Separate known and unknown arguments

    if len(unknown_args) != 3:
        print("Usage: ./file_scan.py [-m] <server> <remote directory> <local mount>")
        sys.exit(1)

    server = unknown_args[0]
    remote_dir = unknown_args[1]
    local_mount = unknown_args[2]

    start_time = time.time()   # Start measuring here

    try:
        fixed_local_mount = f"/mnt/{local_mount}"
        mount_nfs(server, remote_dir, fixed_local_mount)

        directory = f"/mnt/{local_mount}"

        if args.m:   # If -m flag is present
            filename = f"./db/{local_mount}.json"
            files_info = get_media_file_info(directory)
        else:
            filename = f"./db/{local_mount}.json"
            files_info = get_file_info(directory)

        save_as_json(files_info, filename)
    finally:
        unmount_nfs(fixed_local_mount)

    end_time = time.time()   # End measuring here

    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = round((execution_time % 3600) % 60, 2)

    print(f"The script took {hours} hours, {minutes} minutes and {seconds} seconds to execute.")