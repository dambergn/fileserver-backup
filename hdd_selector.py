#!/usr/bin/python3
## Dependencies
# sudo apt install python3-pip
# pip install pyudev

import pyudev
import json
import subprocess

available_devices = []

def list_devices():
    context = pyudev.Context()
    
    for device in context.list_devices(subsystem='block'):
        if 'DEVNAME' in device and device['DEVTYPE'] == 'disk':  # Check if it is a disk device
            devname = device['DEVNAME']
            
            if '/dev/sd' in devname:  # Check if the device name starts with /dev/sd
                # Store the device information as a dictionary
                available_devices.append({
                    'device_node': device.device_node,
                    'sysfs_path': device.sys_path,
                    'properties': dict(device.items())  # Convert to dict for easy access
                })
                
    return available_devices

def get_disk_info(device_node):
    # Get information about all disks
    diskutil_output = subprocess.check_output("diskutil list".split())
    lines = diskutil_output.decode().split("\n")

    for line in lines:
        if device_node not in line:
            continue
        
        # Split the line into parts, usually separated by spaces or tabs
        parts = line.strip().split()
        
        # Get the disk identifier from the first part of the line
        disk_identifier = parts[0].rstrip(":")
        
        # Run 'diskutil info' to get detailed information about this disk
        diskinfo_output = subprocess.check_output(["diskutil", "info", disk_identifier])
        diskinfo_lines = diskinfo_output.decode().split("\n")
        
        details = {}
        
        for line in diskinfo_lines:
            if 'Mount Point:' in line:
                # This is the mount point of the volume
                parts = line.strip().split(":")
                mount_point = parts[1].strip()
                details['mount_point'] = mount_point
                
            elif 'File System Personality:' in line:
                # This tells us if the disk is formatted and what type of file system it uses
                parts = line.strip().split(":")
                fs_personality = parts[1].strip()
                details['formatted'] = fs_personality != 'None'  # If it's not None, then the disk is formatted
                
            elif 'Volume Name:' in line:
                # This is the name of the volume or partition
                parts = line.strip().split(":")
                volume_name = parts[1].strip()
                details['volume_name'] = volume_name
            
            elif 'Disk Size:' in line:
                # This is the size of the disk
                parts = line.strip().split(":")
                disk_size = parts[1].strip()
                details['disk_size'] = disk_size
        
        return details

if __name__ == "__main__":
    devices = list_devices()
    
    # Convert the list of dictionaries into a JSON string
    json_data = json.dumps(devices, indent=4)  # 'indent' argument for pretty printing
    
    print(json_data)  # Print the JSON data

    get_disk_info(json_data)