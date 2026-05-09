import os, subprocess, wget, zipfile, json, shutil

def portablemc(command: str):
    args = command.split()
    process = subprocess.Popen( # Popen даёт динамический вывод данных, а не после завершения
        [os.path.join("bin", "portablemc.exe"), *args],
        stdout=subprocess.PIPE, # "труба" с данными
        stderr=subprocess.STDOUT, # чё бы и нет
        bufsize=1, # какой-то буфер ввода/вывода. Согласно документации, значение 1 заставляет выводить данные буфера построчно.
        text=True)

    for string in process.stdout:
        print(string, end="")
    process.stdout.close()
    return process.wait()
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
            all_instances_dirs = []
            all_instances_names = []
            for directory in os.listdir("instances"):
                if os.path.exists(f"instances/{directory}/pack-info.json"):
                    with open(f"instances/{directory}/pack-info.json", "r", encoding="utf-8") as file:
                        instance_info : dict = json.load(file)
                        all_instances_dirs.append(directory)
                        all_instances_names.append(instance_info["name"])
            if len(all_instances_dirs) == 0:
                print("Нет сборок!")
                pass
            print("НАЗВАНИЕ | ДИРЕКТОРИЯ")
            for i in range(len(all_instances_dirs)):
                print(all_instances_names[i], "|", all_instances_dirs[i] + "/")
            print("Введите название папки...\n> ", end="")

            instance_dir = input()
            with open(f"instances/{instance_dir}/pack-info.json", "r", encoding="utf-8") as file:
                info : directory = json.load(file)
                instance_version = info["version"]
                instance_modloader = info["modloader"]

            portablemc(f"--main-dir %~dp0/../mc_main start -u {nickname} --bin-dir bin --mc-dir %~dp0/../instances/{instance_dir} {instance_modloader}:{instance_version}")
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
        elif x == "3":
            all_instances_dirs = []
            all_instances_names = []
            for directory in os.listdir("instances"):
                if os.path.exists(f"instances/{directory}/pack-info.json"):
                    with open(f"instances/{directory}/pack-info.json", "r", encoding="utf-8") as file:
                        instance_info : dict = json.load(file)
                        all_instances_dirs.append(directory)
                        all_instances_names.append(instance_info["name"])
            if len(all_instances_dirs) == 0:
                print("Нет сборок!")
                pass
            print("НАЗВАНИЕ | ДИРЕКТОРИЯ")
            for i in range(len(all_instances_dirs)):
                print(all_instances_names[i], "|", all_instances_dirs[i] + "/")
            print("Введите название папки...\n> ", end="")

            instance_dir = input()

            if os.path.exists(f"instances/{instance_dir}"):
                if input("Вы точно хотите удалить сборку? Введите 'Yes' без кавычек для подтверждения\n> ") == "Yes":
                    if input("Вы ТОЧНО хотите этого? Введите 'DELETE' без кавычек для подтверждения\n> ") == "DELETE":
                        if input("Последнее предупреждение! Введите 'Sure' без кавычек.\nВСЯ папка сборки будет УНИЧТОЖЕНА БЕЗВОЗРАТНО!\n> ") == "Sure":
                            shutil.rmtree(f"instances/{instance_dir}")
                            if not os.path.exists(f"instances/{instance_dir}"):
                                print("Сборка успешно удалена")
                        else:
                            print("ОТМЕНЕНО")
                    else:
                        print("ОТМЕНЕНО")
                else:
                    print("ОТМЕНЕНО")