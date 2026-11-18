import wmi
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
import pythoncom 

# --- GLOBALS ---
protection_active = False
trusted_devices = set() # Yahan puranay devices ki IDs save hongi

# --- CORE FUNCTIONS ---

def emergency_shutdown():
    """System ko force shutdown karta hai"""
    print("[!!!] SHUTDOWN INITIATED [!!!]")
    time.sleep(3) 
    os.system("shutdown /s /t 0 /f")

def show_blue_alert():
    """Alert Screen"""
    try:
        alert_window = tk.Toplevel()
        alert_window.attributes("-fullscreen", True)
        alert_window.configure(bg="#8B0000") 
        alert_window.attributes("-topmost", True)
        
        tk.Label(alert_window, text="⚠ INTRUSION DETECTED ⚠", font=("Arial", 50, "bold"), bg="#8B0000", fg="white").pack(pady=60)
        tk.Label(alert_window, text="UNAUTHORIZED DEVICE DETECTED", font=("Arial", 30, "bold"), bg="#8B0000", fg="yellow").pack(pady=20)
        
        alert_window.update()
    except:
        pass

def scan_existing_devices():
    """Start mein hi current devices ko 'Trusted List' mein daal deta hai"""
    pythoncom.CoInitialize()
    c = wmi.WMI()
    
    print("--- Scanning Current Devices (Whitelisting) ---")
    # Current connected PnP devices uthao
    for device in c.Win32_PnPEntity():
        if device.DeviceID:
            # Hum sirf DeviceID save karenge (Unique ID)
            trusted_devices.add(device.DeviceID)
            
    print(f"✅ Scanning Complete. {len(trusted_devices)} Devices Trusted.")

def monitor_devices():
    """Background watcher"""
    pythoncom.CoInitialize()
    c = wmi.WMI()
    watcher = c.Win32_PnPEntity.watch_for("creation")
    
    while True:
        try:
            # Wait for NEW event
            device = watcher()
            
            # Agar device ki ID pehle se Trusted List mein hai, to kuch mat karo
            if device.DeviceID in trusted_devices:
                print(f"[SAFE] Known Device Re-detected: {device.Caption}")
                continue # Loop wapis start karo, neechay wala code skip karo

            # --- AGAR YAHAN PUHONCHAY, MATLAB DEVICE "NAYA" HAI ---
            
            if protection_active:
                # Ab check karo ke ye dangerous hai ya nahi (USB/HID/Storage)
                full_info = (str(device.Caption) + " " + str(device.Description) + " " + str(device.DeviceID)).lower()
                
                print(f"[CHECKING NEW DEVICE]: {device.Caption}")

                # Universal Check (USB, Storage, Mouse, Keyboard, Disk)
                if ("usb" in full_info) or ("storage" in full_info) or ("hid" in full_info) or ("disk" in full_info):
                    print(f"!!! NEW UNTRUSTED DEVICE DETECTED !!! -> SHUTTING DOWN")
                    
                    app.after(100, show_blue_alert)
                    
                    t = threading.Thread(target=emergency_shutdown)
                    t.start()
                    
                    break 
            else:
                # Agar protection OFF hai, to is naye device ko bhi Trusted List mein daal do?
                # Nahi, behtar hai sirf ignore karein.
                print(f"[SAFE] New Device (Protection OFF): {device.Caption}")
                
        except Exception as e:
            print(f"[ERROR]: {e}")

def start_protection():
    """Protection ON Button"""
    global protection_active
    
    # Dubara scan karo taake agar user ne abhi kuch lagaya ho to wo trust ho jaye
    threading.Thread(target=scan_existing_devices).start()
    
    protection_active = True
    status_label.config(text="STATUS: ● ARMED (Whitelisted)", fg="green")
    app.iconify()
    messagebox.showinfo("Activated", "System Armed.\nCurrent devices are TRUSTED.\nAny NEW USB will trigger shutdown.")

def stop_protection():
    global protection_active
    protection_active = False
    status_label.config(text="STATUS: ○ DISARMED", fg="red")
    messagebox.showinfo("Deactivated", "Protection OFF.")

# --- GUI SETUP ---
app = tk.Tk()
app.title("Trusted Device Guard")
app.geometry("400x300")
app.configure(bg="#111")

tk.Label(app, text="🛡 TRUSTED USB GUARD", font=("Impact", 20), bg="#111", fg="white").pack(pady=20)
status_label = tk.Label(app, text="STATUS: ○ DISARMED", font=("Consolas", 12), bg="#111", fg="red")
status_label.pack(pady=10)

btn_frame = tk.Frame(app, bg="#111")
btn_frame.pack(pady=20)

start_btn = tk.Button(btn_frame, text="ACTIVATE", font=("Arial", 12, "bold"), bg="green", fg="white", width=12, command=start_protection)
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = tk.Button(btn_frame, text="DEACTIVATE", font=("Arial", 12, "bold"), bg="red", fg="white", width=12, command=stop_protection)
stop_btn.pack(side=tk.RIGHT, padx=10)

# App start hotay hi Pehli Scan karo
first_scan = threading.Thread(target=scan_existing_devices)
first_scan.start()

# Monitoring start karo
monitor_thread = threading.Thread(target=monitor_devices, daemon=True)
monitor_thread.start()

app.mainloop()
