import time
import logging
import json
import threading

import hid


device = hid.device()


def detect_and_update(lock, config_path):

    """
    Проверяет изменился ли product_id мыши, если да - записывает в лист новый айдишник с сохранением старого
    """


    mouse_data = hid.enumerate()
    vid = None
    pid_set = set()
    found_channels = []


    for item in mouse_data:
        if item['manufacturer_string'] == 'ATTACK SHARK':
            vid = item['vendor_id']
            pid_set.add(item['product_id'])



    for item in mouse_data:
        if item['manufacturer_string'] == 'ATTACK SHARK':
            try:
                with lock:
                    device.open_path(item['path'])
                    device.send_feature_report([0, 0, 0, 2, 2, 0, 131] + [0] * 58)
                    for attempt in range(5):
                        time.sleep(0.05)
                        response = device.get_feature_report(0, 65)
                        if response[1] == 161:
                            found_channels.append((item['interface_number'], item['usage_page'], response))
                            break

            except Exception as e:
                logging.error(f"{item['interface_number']} {item['usage_page']} ошибка: {e}")

            finally:
                device.close()
    with lock:
        try:
            with open(config_path, "r", encoding="UTF-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Ошибка чтения конфига ({e}), создаем новый.")
            data = {}
        old_pids = data.get("pid", [])
        data["pid"] = list(set(old_pids) | pid_set)
        data['vid'] = vid
        data.setdefault("battery_report_id", 0)
        data.setdefault("read_retries", 5)
        data.setdefault("read_retry_delay_sec", 0.05)
        with open(config_path, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

    logging.info(f"verification id device: {vid}, product id device : {pid_set}")
    logging.info(f"Рабочие каналы: {found_channels}")


if __name__ == "__main__":
    detect_and_update(threading.Lock(), "config.json")