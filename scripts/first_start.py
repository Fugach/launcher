from .portablemc import install, portablemc
import threading
from PIL import Image



def start():
    pass
def download():
    install()

def login():
    # запускаем логин в лицензионный акк на фоне
    def worker():
        raw_output = portablemc("auth login --output machine", True, False)
    # raw_output = threading.Thread(target=lambda : portablemc("auth login --output machine", True)).start()
    threading.Thread(target=worker, daemon=True).start()

def get_link_and_code(inp):
    print(inp)
    if "auth_device_code" in str(inp):
        print(str(inp).split())
