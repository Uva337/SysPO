# SysAdmin Assistant

Это десктопное приложение на Python и PyQt5, предназначенное для помощи системным администраторам в выполнении рутинных задач на ОС Windows и Astra Linux через графический интерфейс и обработку команд на естественном русском языке (NLU).

## Структура проекта (Упрощенная)

Для надежности импортов структура проекта была сделана "плоской". Все `.py` файлы находятся в одной директории.


.
├── app_new_ui.py             # Главный файл приложения с UI
├── sysadmin_actions.py       # Логика выполнения команд
├── auth_rbac.py              # Аутентификация и контроль доступа
├── command_templates.py      # Управление шаблонами команд
├── logging_audit.py          # Система логирования и аудита
├── macro_engine.py           # Движок для макросов
├── plugin_api.py             # API для плагинов
├── router.py                 # Маршрутизатор интентов
├── utils.py                  # NLU-парсер и утилиты
├── commands.json             # Определения команд и фраз
├── requirements.txt          # Список зависимостей для установки
└── db/                       # Папка для баз данных (создается автоматически)
├── auth.db
└── audit.db


## Установка и запуск

1.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    .\venv\Scripts\activate   # Для Windows
    ```

2.  **Установите зависимости:**
    Скопируйте все файлы проекта в одну папку. Убедитесь, что файл `requirements.txt` находится в ней, и выполните команду:
    ```bash
    pip install -r requirements.txt
    ```
    *Примечание: для `pymorphy2` может потребоваться загрузка словарей при первом использовании.*
    Если при запуске возникает ошибка "A module that was compiled using NumPy 1.x",
    убедитесь, что установлена версия `numpy<2` (она уже прописана в `requirements.txt`).

3.  **Запустите приложение:**
    ```bash
    python app_new_ui.py
    ```

### ❗️ Запуск в Windows с правами администратора

Многие системные команды в Windows (например, `net user`, изменение IP-адреса, управление службами) требуют повышенных прав. Приложение обнаружит, если оно запущено без них, и покажет предупреждение.

Для полноценной работы **настоятельно рекомендуется** запускать приложение от имени администратора. Для этого:
1.  Найдите ваш терминал (PowerShell или Командная строка) в меню "Пуск".
2.  Кликните по нему правой кнопкой мыши.
3.  Выберите **"Запустить от имени администратора"**.
4.  В открывшемся окне перейдите в папку с проектом и запустите его командой `python app_new_ui.py`.

## Первый вход

При первом запуске будут созданы базы данных. Используйте следующие учетные данные для входа:
* **Логин:** `admin`
* **Пароль:** `password123`

## Дополнительные возможности

### Локальный GPT-Neo
Модель GPT-Neo (125M) загружается из директории `models/gpt-neo-125M` (или из каталога,
указанного в переменной окружения `GPT_NEO_PATH`) с использованием
библиотеки `transformers`. Если модель отсутствует, скачайте её с HuggingFace и
расположите по указанному пути. Пример использования:

```python
from offline_gpt import LocalGPTAssistant

assistant = LocalGPTAssistant()
answer = assistant.generate("Как изменить IP в Astra Linux?")
print(answer)
```

### Планировщик задач
Модуль `scheduler.TaskScheduler` позволяет планировать запуск команд во времени.
Задания хранятся в `db/tasks.db` и автоматически выполняются в фоновом потоке.
Пример добавления задачи:

```python
from datetime import datetime, timedelta
from scheduler import TaskScheduler

sched = TaskScheduler(poll_interval=30)
sched.start()
sched.add_task("echo Hello", datetime.now() + timedelta(minutes=1))
```

## Сборка дистрибутива

### Windows

```bat
packaging\windows\build_windows.bat
packaging\windows\package_windows.bat
```
Результат появится в `SysAdminAssistant-win.zip`.

### Debian / AppImage

```bash
./packaging/linux/debian/build_deb.sh
./packaging/linux/appimage/build_appimage.sh
```
После выполнения будут созданы `.deb` и `.AppImage` в каталоге `packaging/linux/`.

## Установка собранного приложения

### Windows

1. Запустите `packaging\windows\build_windows.bat` и затем `packaging\windows\package_windows.bat`.
2. В каталоге `dist` появится папка `SysAdminAssistant-win`, а также архив `SysAdminAssistant-win.zip`.
3. Распакуйте архив в удобное место и запустите `SysAdminAssistant.exe`.

### Astra Linux / Debian

1. С помощью `./packaging/linux/debian/build_deb.sh` соберите пакет `sysadmin-assistant_1.0.0_amd64.deb`.
2. Установите пакет командой:
   ```bash
   sudo dpkg -i sysadmin-assistant_1.0.0_amd64.deb
   ```
3. После установки запустите приложение через меню или командой `sysadmin-assistant`.

## Возможности ChatOps
Во вкладке **ChatOps** можно общаться с локальной моделью GPT-Neo без подключения к интернету. Модель загружается из каталога `models/gpt-neo-125M` при первом использовании.

## Планировщик
На странице "Команды" после выбора команды доступна кнопка **"Запланировать"**. Укажите число минут до запуска, и задача будет сохранена в `db/tasks.db` и выполнена автоматически фоновым планировщиком.

### Портативный AppImage

1. Выполните `./packaging/linux/appimage/build_appimage.sh`.
2. Полученный файл `SysAdminAssistant-1.0.0.AppImage` сделайте исполняемым и запустите:
   ```bash
   chmod +x SysAdminAssistant-1.0.0.AppImage
   ./SysAdminAssistant-1.0.0.AppImage
   ```
