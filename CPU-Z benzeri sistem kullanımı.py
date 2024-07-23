import cpuinfo
import psutil
import wmi
import platform
import tkinter as tk
from tkinter import ttk

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "Brand": info['brand_raw'],
        "Arch": info['arch'],
        "Bits": info['bits'],
        "Count": psutil.cpu_count(logical=False),
        "Logical Count": psutil.cpu_count(logical=True),
        "Frequency": psutil.cpu_freq()._asdict(),
        "L2 Cache": info['l2_cache_size'],
        "L3 Cache": info['l3_cache_size'],
    }

def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    return {
        "Total Memory": virtual_memory.total,
        "Available Memory": virtual_memory.available,
        "Used Memory": virtual_memory.used,
        "Memory Percentage": virtual_memory.percent,
    }

def get_disk_info():
    disk_info = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File System": partition.fstype,
            "Total Size": usage.total,
            "Used": usage.used,
            "Free": usage.free,
            "Percentage": usage.percent,
        })
    return disk_info

def get_system_info():
    system_info = {
        "Platform": platform.system(),
        "Platform Release": platform.release(),
        "Platform Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Processor": platform.processor(),
    }
    # Dinamik olarak ilk ağ arayüzünü kullanarak IP adresi ve MAC adresi bilgilerini ekleyin
    net_if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in net_if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                system_info['IP Address'] = address.address
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                system_info['MAC Address'] = address.address
    return system_info

def get_bios_info():
    c = wmi.WMI()
    bios_info = c.Win32_BIOS()[0]
    return {
        "Manufacturer": bios_info.Manufacturer,
        "Version": bios_info.Version,
        "Release Date": bios_info.ReleaseDate,
    }

def get_motherboard_info():
    c = wmi.WMI()
    board_info = c.Win32_BaseBoard()[0]
    return {
        "Manufacturer": board_info.Manufacturer,
        "Product": board_info.Product,
        "Version": board_info.Version,
    }

def display_info():
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    system_info = get_system_info()
    bios_info = get_bios_info()
    motherboard_info = get_motherboard_info()
    
    # Bilgileri tkinter formunda göster
    root = tk.Tk()
    root.title("System Information")
    
    mainframe = ttk.Frame(root, padding="10 10 10 10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Bilgileri ekleyin
    row = 0
    for title, info in [("CPU Info", cpu_info), 
                        ("Memory Info", memory_info), 
                        ("Disk Info", disk_info), 
                        ("System Info", system_info), 
                        ("BIOS Info", bios_info), 
                        ("Motherboard Info", motherboard_info)]:
        ttk.Label(mainframe, text=title, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W)
        row += 1
        if isinstance(info, list):  # Disk info bir liste ise
            for item in info:
                for key, value in item.items():
                    ttk.Label(mainframe, text=f"{key}: {value}").grid(row=row, column=0, sticky=tk.W, padx=10)
                    row += 1
        else:
            for key, value in info.items():
                ttk.Label(mainframe, text=f"{key}: {value}").grid(row=row, column=0, sticky=tk.W, padx=10)
                row += 1
        row += 1

    root.mainloop()

if __name__ == "__main__":
    display_info()
