# Attack Shark battery charge in Windows tray | Attack Shark заряд прямо в трей Windows

A simple utility that shows your Attack Shark mouse battery charge as an icon in the Windows system tray, with auto-refresh and auto-recovery when the mouse switches connection mode. | Простая утилита, которая показывает заряд батареи мыши Attack Shark прямо в системном трее Windows, с автообновлением и автоопределением при смене режима подключения мыши.

## Features | Возможности

- Reads battery percentage and charging status directly over USB HID (no official SDK needed) | Читает процент заряда и статус зарядки напрямую через USB HID, без официального SDK
- Live tray icon tooltip, updated every few seconds | Живой tooltip иконки в трее, обновляется каждые несколько секунд
- Auto-detects your mouse's VID/PID — no manual configuration needed | Автоматически находит VID/PID твоей мыши — ручная настройка не нужна
- Automatically re-scans in the background, so it keeps working even if the mouse's PID changes (e.g. when placed on charge) | Автоматически пересканирует устройство в фоне, поэтому продолжает работать даже если PID мыши меняется (например, при постановке на зарядку)
- Runs as a standalone .exe, no Python installation required | Работает как самостоятельный .exe, установка Python не требуется
- Logs to a file instead of a console window, so it can run silently in the background | Пишет логи в файл вместо консоли — можно запускать полностью в фоне

## Requirements | Требования

- Windows 10/11
- An Attack Shark mouse connected via its 2.4G wireless dongle. Confirmed working: R5 Ultra, M5 Ultra (appears to be effectively the same mouse/protocol as the R5 Ultra). Not personally tested: R6, R8 — may share the same protocol based on community documentation, but this is unverified. | Мышь Attack Shark, подключённая через 2.4G-донгл. Подтверждено рабочими: R5 Ultra, M5 Ultra (судя по всему, по сути та же мышь/протокол, что и R5 Ultra). Лично не проверялись: R6, R8 — вероятно используют тот же протокол согласно документации сообщества, но это не подтверждено.
- Python 3.10+ — only if running from source, not needed for the .exe | Python 3.10+ — только если запускаешь из исходников, для .exe не требуется

## How to install | Как установить

### Option 1 — prebuilt .exe | Вариант 1 — готовый .exe

1. Download `main.exe` from the [Releases](../../releases) page | Скачай `main.exe` со страницы [Releases](../../releases)
2. Run it — `config.json` will be created automatically next to the .exe on first launch | Запусти его — `config.json` создастся автоматически рядом с .exe при первом запуске
3. Look for the mouse icon in the system tray (check the hidden icons arrow `^` if you don't see it) | Найди иконку мыши в системном трее (загляни в скрытые значки `^`, если сразу не видно)

### Option 2 — from source | Вариант 2 — из исходников

```bash
git clone <repo-url>
cd attack-shark-r5-ultra-gui-windows
pip install -r requirements.txt
python main.py
```

`config.json` is generated automatically on first run. See `config.example.json` for the expected structure. | `config.json` создаётся автоматически при первом запуске. Структуру смотри в `config.example.json`.

### Building the .exe yourself | Собрать .exe самостоятельно

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --add-data "src/mouse_image.png;src" main.py
```

The resulting `main.exe` will be in the `dist/` folder. | Готовый `main.exe` окажется в папке `dist/`.

## Autostart | Автозагрузка

To launch automatically at Windows startup: | Чтобы запускалось автоматически при старте Windows:

1. Press `Win + R`, type `shell:startup`, hit Enter | Нажми `Win + R`, введи `shell:startup`, Enter
2. Create a shortcut to `main.exe` and place it in that folder | Создай ярлык на `main.exe` и помести его в эту папку

## How it works | Как это работает

The mouse's battery status is queried over a vendor-specific USB HID feature report — the same channel used by the official companion software, reverse-engineered by the community rather than documented officially. `device_detect.py` automatically finds the correct VID/PID/HID channel for your specific mouse and writes it to `config.json`; `main.py` polls it periodically and updates the tray tooltip. | Статус батареи мыши считывается через вендорский USB HID feature-репорт — тот же канал, что использует официальное фирменное ПО, реверс-инжинерен сообществом, а не задокументирован официально. `device_detect.py` автоматически находит нужные VID/PID/HID-канал для конкретно твоей мыши и записывает их в `config.json`; `main.py` периодически опрашивает их и обновляет tooltip в трее.

## Known limitations | Известные ограничения

- Only supports Attack Shark mice — the protocol is vendor-specific and won't work with other brands. Only R5 Ultra were personally tested; other models are untested | Поддерживает только мыши Attack Shark — протокол специфичен для этого производителя и не подойдёт для других брендов. Лично протестированы только R5 Ultra; остальные модели не проверялись

## License | Лицензия

MIT
