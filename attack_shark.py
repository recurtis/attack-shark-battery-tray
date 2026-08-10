import hid
import time
import json
import logging


device = hid.device()


def attack_shark_get_battery(lock, config_path):
    """
    Опрашивает мышь по HID и возвращает статус батареи.
    Возвращает (charging, percent) или (None, None), если не удалось прочитать.
    """
    with open(config_path) as file:
        config = json.load(file)


    for pid in config['pid']:
        mouse_info = hid.enumerate(config['vid'], pid)

        for item in mouse_info:

            if item["usage_page"] == 65535:

                if item["interface_number"] == 2:

                    try:
                        with lock:
                            device.open_path(item['path'])
                            device.send_feature_report([config['battery_report_id'], 0, 0, 2, 2, 0, 131] + [0] * 58)

                            for attempt in range(config['read_retries']):
                                time.sleep(config['read_retry_delay_sec'])
                                response = device.get_feature_report(config['battery_report_id'], 65)

                                if response[1] == 161:
                                    return response[7], response[8]
                        
                    except Exception as e:
                        logging.error(f"{item['interface_number']} {item['usage_page']} ошибка: {e}")

                    finally:
                        device.close()
    return None, None