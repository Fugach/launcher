import os, subprocess, shlex, sys, wget, zipfile, shutil
from traceback import extract_tb


def portablemc(command: str):
    args = shlex.split(command)
    return subprocess.run(
        [sys.executable, "-m", "portablemc", *args],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
def install():
    if not os.path.isfile("portablemc.exe"):
        print("Downloading portablemc...")
        wget.download(
            "https://github.com/theorzr/portablemc/releases/download/v5.0.3/portablemc-5.0.3-windows-x86_64-msvc.zip",\
            "portablemc-5.0.3-windows-x86_64-msvc.zip")
        print("\nDone. Unzipping...")
        with zipfile.ZipFile("portablemc-5.0.3-windows-x86_64-msvc.zip", "r") as zip:
            zip.extract("portablemc.exe")
        os.remove("portablemc-5.0.3-windows-x86_64-msvc.zip")
        print("Now portablemc is here!")
    else:
        print("portablemc is already here!")
    if not os.path.isdir("bin"):
        os.makedirs("bin")
    if not os.path.isdir("mc_main"):
        os.makedirs("mc_main")

if __name__ == "__main__":
    install()