import os
import threading
import time
import device_detect
import attack_shark
import sys
import logging

import pystray
import PIL.Image

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

lock = threading.Lock()
img_path = os.path.join(BASE_DIR, "src", "mouse_image.png")
image = PIL.Image.open(img_path)


if getattr(sys, 'frozen', False):
    config_dir = os.path.dirname(sys.executable)
else:
    config_dir = os.path.dirname(__file__)
config_path = os.path.join(config_dir, "config.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=os.path.join(config_dir, "app.log"),
    encoding="utf-8"
)


def exit_action(icon_obj, item):    
    icon.stop()
menu = pystray.Menu(
    pystray.MenuItem("Выход", exit_action)
)
icon = pystray.Icon("mouse", image, title = 'text', menu = menu)




def update_config():
    while True:
        device_detect.detect_and_update(lock, config_path)
        time.sleep(300)


def update_loop():
    """
    Опрашивает мышь и меняет значения взависимости от того поменялся ли заряд и поставилась ли мышь на зарядку
    """
    while True:
        charging, percent = attack_shark.attack_shark_get_battery(lock, config_path)
        if charging == 0:
            icon.title = f"Мышка не на зарядке\nПроцента заряда: {percent}%"
        elif charging == 1:
            icon.title = f"Мышка на зарядке\nПроцента заряда: {percent}%"
        time.sleep(5)



if __name__ == "__main__":
    device_detect.detect_and_update(lock, config_path)
    thread1 = threading.Thread(target=update_loop, daemon=True)
    thread2 = threading.Thread(target=update_config, daemon=True)
    thread1.start()
    thread2.start()
    icon.run()

