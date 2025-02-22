# LayerEdge Auto

**LayerEdge Auto** – это проект для автоматизации работы с платформой LayerEdge. Он включает регистрацию аккаунтов, фарминг (24/7), получение реферальных кодов и пинг-бот для ежедневной активности. Проект позволяет запускать фарминг сразу после регистрации, а при остановке – возобновлять его, перемещая приватные ключи из `results/success.txt` в `configs/farm.txt` и установив в `configs/config.py` параметр `FARM_MODE = True`.

![photo_2025-02-16_21-21-21](https://github.com/user-attachments/assets/8e1be1e6-01e7-43a2-aec4-055cf8b704ce)
---

## Требования

- **Python 3.9** или выше  
- **pip**  
- **Git** (опционально)  
- Для Windows: если возникает ошибка с модулем `curses`, установите пакет:
  ```bash
  pip install windows-curses
  ```

---

## Установка и настройка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/k2wGG/layeredge-bot.git
cd layeredge-bot
```

### 2. Создайте виртуальное окружение (опционально)

**На Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**На Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте конфигурационные файлы

- **Приватные ключи для регистрации:**  
  Поместите ваши приватные ключи в файл:  
  `configs/register.txt`  
  (Один ключ – в одной строке)

- **Прокси-серверы:**  
  Поместите ваши прокси в файл:  
  `configs/proxies.txt`  
  В формате:
  ```
  http://login:password@ip:port
  ```
  
- **Реферальные коды:**  
  Добавьте реферальные коды в файл:  
  `configs/REFS.txt`

- **Приватные ключи для фарма:**  
  Если вы планируете использовать уже зарегистрированные аккаунты для фарминга, поместите их в файл:  
  `configs/farm.txt`

- **Конфигурация:**  
  Откройте файл `configs/config.py` и настройте параметры, например:
  - Задержки перед стартом (MIN_DELAY_BEFORE_START, MAX_DELAY_BEFORE_START)
  - Параметры рефералов (DAYS, HOURS, MINUTES)
  - SSL-проверку (SSL)
  
  Если вы хотите, чтобы после регистрации аккаунты сразу начинали фармить, убедитесь, что:
  ```python
  FARM_MODE = True
  ```
  Если режим регистрации используется отдельно – настройте флаги по вашему усмотрению.

### 5. Запустите установочные скрипты

Согласно инструкциям, выполните:
- **Запустите INSTALL.txt** (следуйте инструкциям в файле INSTALL.txt для первичной установки)
- **Запустите START.txt** (этот скрипт поднимет проект)

---

## Режимы работы

После регистрации аккаунтов проект сразу начинает фарминг – вам не нужно перезапускать программу для его запуска.  
Если вы остановите фарминг, чтобы возобновить работу, переместите приватные ключи из файла `results/success.txt` в `configs/farm.txt` и убедитесь, что в `configs/config.py` установлен параметр `FARM_MODE = True`.

**Основные режимы:**

1. **Регистрация аккаунтов:**  
   Читает приватные ключи из `configs/register.txt` и регистрирует их на платформе LayerEdge.

2. **Фарм 24/7:**  
   Запускается сразу после регистрации (если включён режим FARM_MODE) и выполняется в бесконечном цикле – выполняется чек-ин, перезапуск узла и фарминг по заданным задержкам.

3. **Получение реферальных кодов:**  
   Для получения реферальных кодов используется файл `configs/REFS.txt`.

4. **Пинг-бот, ежедневный чек-ин:**  
   Дополнительный режим для однократного обновления состояния узла (пинг) и проверки активности.

---

## Запуск проекта

После выполнения всех вышеописанных шагов запустите проект из корневой директории:

```bash
python main.py
```


Выберите нужный режим, и программа выполнит соответствующие действия.

---

## Дополнительная информация

- **Логи:**  
  Логи сохраняются в папке `log` и выводятся в консоль.  
- **База данных:**  
  Файл базы данных создаётся в папке `data` (путь указан в `configs/constants.py`).

- **Перезапуск фарминга:**  
  Если фарминг остановлен, переместите приватные ключи из `results/success.txt` в `configs/farm.txt` и установите `FARM_MODE = True` в `configs/config.py`.

---
