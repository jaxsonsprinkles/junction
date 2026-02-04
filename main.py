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


def close_app(exe):
    matches = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            name = proc.info.get('name') or ''
            if exe.lower() in name.lower():
                matches.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not matches:
        print("App not running")
        return

    for proc in matches:
        proc.terminate()


def search(name):
    for app in programs:
        if app.get("name") == name and app.get("path") is not None:
            return app


def create_mode(*args):
    apps = []
    for program in args:
        details = search(program)
        if details:
            apps.append(details)
        else:
            print(program + " not found")
    return apps


def open_mode(mode):
    for program in mode:
        open_app(program.get("exe"), program.get("path"))

def switch_mode(close, open):
    for program in close:
        close_app(program.get("exe"))
    for program in open:
        open_app(program.get("exe"), program.get("path"))

programs = list_programs()
print(programs)

relax = create_mode("LocalSend version 1.17.0")
study = create_mode("Google Chrome", "Cursor")

switch_mode(relax, study)
