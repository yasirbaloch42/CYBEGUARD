# 🛡️ Duck Hunter - USB HID Intrusion Detection System

**Duck Hunter** is a Python-based endpoint security tool designed to protect systems against malicious USB Human Interface Device (HID) attacks, commonly known as **USB Rubber Ducky** or **BadUSB** attacks.

Unlike traditional antivirus software that trusts all HID devices (Keyboards/Mice), Duck Hunter monitors the system for unauthorized device connections in real-time. Upon detecting an unknown HID device while armed, it triggers an immediate defensive response to prevent payload execution.

## 🚀 Key Features

* **Real-time Monitoring:** Continuously watches for new USB device events using Windows Management Instrumentation (WMI).
* **Automated Defense:** Instantly detects devices classifying themselves as "Keyboard" or "Mouse".
* **Visual Alert:** Displays a full-screen "Red/Blue Alert" to warn the user.
* **Kill Switch:** Initiates an emergency system shutdown to cut power and stop the malicious script from executing commands.
* **Control Panel:** GUI-based Activate/Deactivate mechanism to allow legitimate device insertion.
* **Stealth Mode:** Runs in the background without obstructing the user's workflow.

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **GUI:** Tkinter
* **System Interface:** WMI (Windows Management Instrumentation)
* **Concurrency:** Python Threading & Pythoncom

## 📋 Prerequisites

Before running the application, ensure you have Python installed. You also need to install the required dependencies:

```bash
pip install wmi pywin32

## run :  python cybeguard.pyw