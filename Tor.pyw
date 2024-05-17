import customtkinter as ctk
from tkinter import messagebox
import subprocess
import psutil  

tor_process = None
subprocess.Popen(["taskkill", "/F", "/IM", "tor.exe"], creationflags=subprocess.CREATE_NO_WINDOW)

def run_tor():
    global tor_process
    try:
        tor_process = subprocess.Popen(["tor.exe", "-f", "torrc"], creationflags=subprocess.CREATE_NO_WINDOW)
        messagebox.showinfo("Tor Status", "Tor started successfully!")
        update_tor_status() 
    except FileNotFoundError:
        messagebox.showerror("Error", "Tor executable or configuration file not found!")

def stop_tor():
    global tor_process
    if tor_process:
        if tor_process.poll() is None: 
            try:
                tor_process.terminate() 
                tor_process.wait(timeout=5)  
                if tor_process.poll() is None: 
                    subprocess.Popen(["taskkill", "/F", "/IM", "tor.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
                messagebox.showinfo("Tor Status", "Tor stopped successfully!")
                update_tor_status()  
            except subprocess.TimeoutExpired:
                messagebox.showerror("Error", "Failed to stop Tor gracefully, using forceful termination.")
        else:
            messagebox.showinfo("Tor Status", "Tor is not currently running.")
    else:
        subprocess.Popen(["taskkill", "/F", "/IM", "tor.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
        messagebox.showinfo("Tor Status", "Tor stopped successfully!")

def update_tor_status():
    global tor_process
    tor_running = tor_process is not None and tor_process.poll() is None

    status_label.configure(text="Tor Status: " + ("Running" if tor_running else "Stopped"))

root = ctk.CTk()
root.title("Tor VPN Controller")

status_label = ctk.CTkLabel(root, text="Tor Status: Unknown", width=250)
status_label.pack(pady=10, padx=20)

start_button = ctk.CTkButton(
    root, text="Start Tor", command=run_tor, width=120, height=40
)
start_button.configure(fg_color="green", bg_color="green", border_width=2, corner_radius=8)
stop_button = ctk.CTkButton(
    root, text="Stop Tor", command=stop_tor, width=120, height=40
)
stop_button.configure(fg_color="red", bg_color="red", border_width=2, corner_radius=8)
start_button.pack(side=ctk.LEFT, padx=20, pady=10)
stop_button.pack(side=ctk.RIGHT, padx=20, pady=10)

update_tor_status()

root.mainloop()
