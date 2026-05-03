from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
import os, subprocess, wget, zipfile, json

def portablemc(command: str):
    args = command.split()
    process = subprocess.run(
        [os.path.join("bin", "portablemc.exe"), *args], capture_output=True)
    try:
        stdout = process.stdout.decode("utf-8")
        stderr = process.stderr.decode("utf-8")
    except UnicodeDecodeError:
        stdout = process.stdout.decode("cp1251", errors="replace")
        stderr = process.stderr.decode("cp1251", errors="replace")
    return process.returncode, stdout, stderr
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
    # snapshot, alpha, beta, release...
    all_blacklist = ["+00:00", "name", "channel", "release_date", "row", "sep"]
    if channel != "":
        output = list(portablemc("search --channel " + channel + " --output machine").stdout.split())
    else:
        for x in ["release", "release*", "snapshot", "beta", "alpha"]:
            all_blacklist.append(x)
        output = list(portablemc("search --output machine").stdout.split()) # каждая версия включая тег
    output = [item for item in output if not any(x in item for x in all_blacklist)]
    return output

nickname : str = "123"

if __name__ == "__main__":
    install()
    print("!!! пока что интерфейс только текстовый !!!")
    print("Что сделать?\n1. Запустить сборку\n2. Создать сборку\n3. Удалить сборку\n Введите номер... ")
    while True:
        x = input("> ")
        if x == "1":
            all_instances = os.listdir("instances")

            num = 1
            for y in all_instances:
                print(str(num) + ".", y)
                num += 1

            print("Выберите сборку...\n> ", end="")
            portablemc(f"--main-dir %~dp0/../../mc_main start -u {nickname} --bin-dir bin --mc-dir %~dp0/../../instances/{str(all_instances[int(input()) - 1])} mojang:b1.7.3")
            exit(0)
        elif x == "2":
            name = input("Введите название...\n> ")
            version = input("Выберите версию...\n> ")
            modloader = input("Выберите загрузчик модов, например, forge, fabric, neoforge, quilt...\n> ")

            install_dir = f"instances/{name}"

            if not os.path.isdir(install_dir):
                os.makedirs(install_dir)
            else:
                num = 1
                while os.path.isdir(install_dir + str(num)):
                    num += 1
                os.makedirs(install_dir + str(num))
                install_dir += str(num)

            with open(f"{install_dir}/pack-info.json", "w", encoding="utf-8") as file:
                json.dump({
                    "name" : name,
                    "version" : version,
                    "modloader" : modloader
                }, file, ensure_ascii=False, indent=2)
            print(f"Готово! Папка находится по пути {install_dir}.")