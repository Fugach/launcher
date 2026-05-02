from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
import os, subprocess, wget, zipfile

def portablemc(command: str):
    args = command.split()
    return subprocess.run(
        [os.path.join("bin", "portablemc.exe"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
def install():
    if not os.path.exists("bin/portablemc.exe"):
        print("Downloading portablemc...")
        wget.download(
            "https://github.com/theorzr/portablemc/releases/download/v5.0.3/portablemc-5.0.3-windows-x86_64-msvc.zip",\
            "portablemc-5.0.3-windows-x86_64-msvc.zip")
        print("\nDone. Unzipping...")
        with zipfile.ZipFile("portablemc-5.0.3-windows-x86_64-msvc.zip") as zip:
            zip.extract("portablemc.exe")
        os.remove("portablemc-5.0.3-windows-x86_64-msvc.zip")
        if not os.path.isdir("bin"):
            os.makedirs("bin")
        os.replace("portablemc.exe", "bin/portablemc.exe")
        print("Now portablemc is here!")
    else:
        print("portablemc is already here!")
    if not os.path.isdir("mc_main"):
        os.makedirs("mc_main")
    if not os.path.isdir("instances"):
        os.makedirs("instances")
def get_versions(channel):
    output = list(portablemc("search --channel " + channel + " --output machine").stdout.split())
    output = [item for item in output if not any(x in item for x in ["+00:00", "name", "channel", "release_date", "row", "sep", channel])]
    return output
if __name__ == "__main__":
    install()
    get_versions("alpha")