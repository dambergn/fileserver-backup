#!/usr/bin/python3
import subprocess
import sys

def list_devices():
    result = subprocess.run(['lsblk', '-dn', '-o', 'NAME,SIZE,TYPE'], capture_output=True, text=True)
    devices = [line.split() for line in result.stdout.strip().split('\n') if 'disk' in line]
    return devices

def format_device(device, label):
    try:
        # Create a new partition table
        subprocess.run(['sudo', 'parted', '-s', f'/dev/{device}', 'mklabel', 'gpt'], check=True)

        # Create a new partition
        subprocess.run(['sudo', 'parted', '-s', f'/dev/{device}', 'mkpart', 'primary', '0%', '100%'], check=True)

        # Format the partition to exFAT
        subprocess.run(['sudo', 'mkfs.exfat', '-n', label, f'/dev/{device}1'], check=True)

        print(f"Device /dev/{device}1 formatted to exFAT with label '{label}'")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting device: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 format_exfat.py <device> <label>")
        print("Example: python3 format_exfat.py sdb MyLabel")
        sys.exit(1)

    device = sys.argv[1]
    label = sys.argv[2]

    devices = list_devices()
    available_devices = [dev[0] for dev in devices]

    if device not in available_devices:
        print(f"Device {device} not found. Available devices:")
        for dev in devices:
            print(f"/dev/{dev[0]} ({dev[1]})")
        sys.exit(1)

    format_device(device, label)