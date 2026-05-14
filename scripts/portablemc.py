import os, subprocess, wget, zipfile

def portablemc(command : str, echo : bool, show : bool) -> str: # стрелочка и str даёт понимать ide, что нужно вернуть ИМЕННО СТРОКУ, удобно
    # P.S. видимо в IDLE не поддерживает подобных приколов с двоеточием, а pycharm их спокойно переваривает
    # либо я что-то не так понял
    # или информатик
    portablemc_path = os.path.join("bin", "portablemc.exe")
    cmd_args = [portablemc_path] + command.split()
    with subprocess.Popen( # Popen даёт динамический вывод данных, а не после завершения
        cmd_args, # аргументы
        cwd="bin", # из какой директории выполняется подпроцесс
        stdin=subprocess.PIPE if echo else None, # если echo, то можно ввести сразу ещё что-то, например enter
        # в данный момент времени вводится enter
        stdout=subprocess.PIPE, # "труба" с данными
        stderr=subprocess.STDOUT, # чё бы и нет
        bufsize=1, # какой-то буфер ввода/вывода. Согласно документации, значение 1 заставляет выводить данные буфера построчно.
        text=True) as process:

        if echo and process.stdin: # <= вот здесь вводится enter, если echo == True и разрешён доп. ввод !!!!!
            process.stdin.write("\n")
            process.stdin.close()
        output = []
        for string in process.stdout:
            output.append(string)
            if show:
                print("[ PORTABLEMC ]", string, end="")

        return "".join(output)

def install():
    if not os.path.exists("bin/portablemc.exe"):
        print("Скачиваем portablemc...")
        wget.download(
            "https://github.com/theorzr/portablemc/releases/download/v5.0.3/portablemc-5.0.3-windows-x86_64-msvc.zip",\
            "portablemc-5.0.3-windows-x86_64-msvc.zip")
        print("Готово. Распаковываем...")
        with zipfile.ZipFile("portablemc-5.0.3-windows-x86_64-msvc.zip") as zip:
            zip.extract("portablemc.exe")
        os.remove("portablemc-5.0.3-windows-x86_64-msvc.zip")
        if not os.path.isdir("bin"):
            os.makedirs("bin")
        os.replace("portablemc.exe", "bin/portablemc.exe")
        print("Теперь portablemc здесь!")
    else:
        print("portablemc уже здесь! Установка не требуется!")
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