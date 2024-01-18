# AUTHOR  = PRYMIE SOFTWARE 
# VERSION = 1.0
# DESCRIPTION = Dosyalarınızı Otomatik Olarak Backup Alın.
# WEBSITE = prymiesoftware.web.tr

# ____                       _               
#|  _ \ _ __ _   _ _ __ ___ (_) ___          
#| |_) | '__| | | | '_ ` _ \| |/ _ \         
#|  __/| |  | |_| | | | | | | |  __/                                          
#|_|   |_|   \__, |_| |_| |_|_|\___|         
# ____       |___/_                          
#/ ___|  ___  / _| |___      ____ _ _ __ ___ 
#\___ \ / _ \| |_| __\ \ /\ / / _` | '__/ _ \
# ___) | (_) |  _| |_ \ V  V / (_| | | |  __/
#|____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|
#                    _                   _  _   _       _                
#_ __ ___   __ _  __| | ___  __      _  (_)| |_| |__   | | _____   _____ 
#| '_ ` _ \ / _` |/ _` |/ _ \ \ \ /\ / /| || __| '_ \  | |/ _ \ \ / / _ \
#| | | | | | (_| | (_| |  __/  \ V  V / | || |_| | | | | | (_) \ V /  __/
#|_| |_| |_|\__,_|\__,_|\___|   \_/\_/  |_| \__|_| |_| |_|\___/ \_/ \___|

import os
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

def backup():
    backup_thread = threading.Thread(target=perform_backup)
    backup_thread.start()

def select_backup_folder():
    backup_folder = filedialog.askdirectory()
    if backup_folder:
        backup_folder_var.set(backup_folder)

def update_progress():
    progress_bar["value"] += 1
    root.update_idletasks()

def perform_backup():
    backup_folder = backup_folder_var.get()

    total_dirs = sum([var_program_data.get(), var_program_files.get(), var_appdata.get(), var_desktop.get(),
                      var_downloads.get(), var_documents.get(), var_videos.get()])
    if total_dirs == 0 or not backup_folder:
        messagebox.showinfo("Backup", "Please select at least one directory to backup and choose a backup folder.")
        return

    progress_bar["maximum"] = total_dirs
    progress_bar["value"] = 0

    dirs_to_backup = []
    if var_program_data.get():
        dirs_to_backup.append(os.path.join(os.environ['ProgramData']))
    if var_program_files.get():
        dirs_to_backup.append(os.path.join(os.environ['ProgramFiles']))
    if var_appdata.get():
        dirs_to_backup.append(os.path.join(os.environ['USERPROFILE'], '.appdata'))
    if var_desktop.get():
        dirs_to_backup.append(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
    if var_downloads.get():
        dirs_to_backup.append(os.path.join(os.environ['USERPROFILE'], 'Downloads'))
    if var_documents.get():
        dirs_to_backup.append(os.path.join(os.environ['USERPROFILE'], 'Documents'))
    if var_videos.get():
        dirs_to_backup.append(os.path.join(os.environ['USERPROFILE'], 'Videos'))

    backup_file = os.path.join(backup_folder, 'backup.zip')

    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for dir_to_backup in dirs_to_backup:
            for root, _, files in os.walk(dir_to_backup):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_path = os.path.relpath(file_path, os.path.join(os.environ['USERPROFILE'], '.appdata'))
                    zipf.write(file_path, zip_path)

                    # Update progress bar for each file
                    update_progress()

    # Print success message
    messagebox.showinfo("Backup", "Backup completed!")

root = tk.Tk()
root.title("Backup")

# İkon eklemek için .ico dosyasını belirtin
icon_path = "assets/icon/prymie.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

backup_folder_var = tk.StringVar()

var_program_data = tk.BooleanVar()
var_program_files = tk.BooleanVar()
var_appdata = tk.BooleanVar()
var_desktop = tk.BooleanVar()
var_downloads = tk.BooleanVar()
var_documents = tk.BooleanVar()
var_videos = tk.BooleanVar()

ttk.Checkbutton(root, text="Program Data", variable=var_program_data).grid(column=0, row=0, sticky=tk.W)
ttk.Checkbutton(root, text="Program Files", variable=var_program_files).grid(column=0, row=1, sticky=tk.W)
ttk.Checkbutton(root, text="AppData", variable=var_appdata).grid(column=0, row=2, sticky=tk.W)
ttk.Checkbutton(root, text="Desktop", variable=var_desktop).grid(column=0, row=3, sticky=tk.W)
ttk.Checkbutton(root, text="Downloads", variable=var_downloads).grid(column=0, row=4, sticky=tk.W)
ttk.Checkbutton(root, text="Documents", variable=var_documents).grid(column=0, row=5, sticky=tk.W)
ttk.Checkbutton(root, text="Videos", variable=var_videos).grid(column=0, row=6, sticky=tk.W)

backup_folder_entry = ttk.Entry(root, textvariable=backup_folder_var, state='readonly')
backup_folder_entry.grid(column=0, row=7, pady=5, sticky=tk.W)
ttk.Button(root, text="Select Backup Folder", command=select_backup_folder).grid(column=1, row=7, pady=5, sticky=tk.W)

backup_button = ttk.Button(root, text="Backup", command=backup)
backup_button.grid(column=0, row=8, columnspan=2, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(column=0, row=9, columnspan=2, pady=10)

root.mainloop()
