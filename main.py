import assets.scripts.first_start

from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

PORTABLEMC_DIR = Path(__file__).parent / 'bin' / 'portablemc.exe'
TEXTURES_DIR = Path(__file__).parent / 'assets' / 'textures'
PROFILES_DIR = Path(__file__).parent / 'profiles.txt'

print('-' * 55)
print('TEXTURES_DIR     |', TEXTURES_DIR)
print('PORTABLEMC_DIR   |', PORTABLEMC_DIR)
print('PROFILES_DIR     |', PROFILES_DIR)
print('-' * 55)

if __name__ == "__main__":
    if not PORTABLEMC_DIR.is_file() or not PROFILES_DIR.is_file():
        assets.scripts.first_start.start()

    loader
    # print("!!! пока что интерфейс только текстовый !!!")
    # print("--------------------------------------------\nЧто сделать?\n1. Запустить сборку\n2. Создать сборку\n3. Удалить сборку\n Введите номер... ")
    while False:
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
                info : dict = json.load(file)
                instance_version = info["version"]
                instance_modloader = info["modloader"]

            portablemc(f"--main-dir %~dp0/../mc_main start -u {nickname} --bin-dir bin --mc-dir %~dp0/../instances/{instance_dir} {instance_modloader}:{instance_version}", False)
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
                    if input("Папка сборки будет перемещена в корзину! Введите 'DELETE' без кавычек для подтверждения\n> ") == "DELETE":
                        send2trash.send2trash(f"instances/{instance_dir}")
                        if not os.path.exists(f"instances/{instance_dir}"):
                            print("Сборка успешно удалена")
                        else:
                            print("что-то пошло не так")
                    else:
                        print("ОТМЕНЕНО")
                else:
                    print("ОТМЕНЕНО")