#!/usr/bin/python3
## Dependencies
# sudo apt install python3-pip
# pip install pyudev

import json
# import psutil
# import pyudev
from pyudev import Devices, Context
import subprocess

def get_device_info():
    devices = []

    try:
        # Get detailed information about all block devices
        lsblk_output = subprocess.check_output(
            ["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,TRAN", "-J"],
            universal_newlines=True
        )
        lsblk_data = json.loads(lsblk_output)

        # Filter only SATA and USB devices
        for blockdevice in lsblk_data["blockdevices"]:
            if blockdevice["type"] == "disk" and blockdevice["tran"] in ["sata", "usb"]:
                device_info = {
                    "device": f"/dev/{blockdevice['name']}",
                    "device_size": blockdevice["size"],
                    "type": blockdevice["tran"],  # Include the transport type (sata or usb)
                    "partitions": []  # List to hold partitions information
                }

                # Check if this device has partitions and gather their information
                if "children" in blockdevice:
                    for child in blockdevice["children"]:
                        partition_info = {
                            "partition": f"/dev/{child['name']}",
                            "size": child["size"],
                            "mountpoint": child.get("mountpoint", None),
                            "filesystem": child.get("fstype", "Unknown")
                        }
                        device_info["partitions"].append(partition_info)

                devices.append(device_info)
    except subprocess.CalledProcessError:
        print("Error occurred while executing lsblk command")

    return devices

def main():
    devices_info = get_device_info()
    print(json.dumps(devices_info, indent=4))

if __name__ == "__main__":
    main()