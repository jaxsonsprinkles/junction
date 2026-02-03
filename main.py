import winreg
import os
import subprocess
import psutil
import winapps


def list_programs():
    blacklist = ['unins000.exe', 'svchost.exe', 'conhost.exe']
    program_list = []
    for app in winapps.list_installed():

        try:
            for name in os.listdir(app.install_location):
                if name.lower().endswith(".exe") and name.lower() not in blacklist:
                    program_list.append({
                        "name": app.name,
                        "path": os.path.join(app.install_location, name),
                        "exe": name
                    })
                    break

        except Exception:
            pass

    return program_list


def is_app_open(exe):
    for proc in psutil.process_iter(['name']):
        try:
            if exe.lower() in proc.info['name'].lower():

                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return False


def open_app(exe, path):
    if not is_app_open(exe):

        try:
            subprocess.Popen(path)
        except FileNotFoundError:
            print("Error: Program not found")
    else:
        print("Program " + exe + " already running")


def search(name):
    for app in programs:
        if app.get("name") == name and app.get("path") is not None:
            return app


programs = list_programs()

program = search("Audacity 3.1.3")

open_app(program.get("exe"), program.get("path"))
