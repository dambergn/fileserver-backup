#!/usr/bin/python3
import subprocess
import psutil

def get_storage_devices():
    partitions = psutil.disk_partitions(all=True)
    devices = [partition.device for partition in partitions if 'removable' in partition.opts or 'rw' in partition.opts]
    return devices

def format_to_exfat(device, label):
    try:
        # Unmount the device (if necessary)
        subprocess.run(['umount', device], check=True)

        # Format the device to exFAT
        subprocess.run(['mkfs.exfat', '-n', label, device], check=True)

        print(f"Device {device} formatted to exFAT with label '{label}'")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting device: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    devices = get_storage_devices()
    if not devices:
        print("No removable storage devices found.")
    else:
        print("Available devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device}")

        device_index = int(input("Enter the number of the device you want to format: "))
        device = devices[device_index]

        label = input("Enter the custom name for the partition: ")

        format_to_exfat(device, label)