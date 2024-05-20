#!/usr/bin/python3
## Dependencies
# pip install pyudev

import pyudev


def list_devices():
    context = pyudev.Context()
    
    for device in context.list_devices(subsystem='block'):  # List all storage devices
        print(f"Device Node: {device.device_node}")
        print(f"Sysfs Path: {device.sys_path}")
        
        for key, value in device.items():   # Print out the device properties
            print(f"{key}: {value}")
            
        print()  # Add a newline after each device for readability

if __name__ == "__main__":
    list_devices()