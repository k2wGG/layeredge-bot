import os

def move_account_to_farm(private_key, source_path, dest_path):
    """
    Перемещает приватный ключ из файла source_path в файл dest_path.
    
    Если ключ уже присутствует в dest_path, он не добавляется повторно.
    После перемещения, ключ удаляется из source_path.
    
    :param private_key: Строка с приватным ключом.
    :param source_path: Путь к файлу с успешно зарегистрированными аккаунтами (например, results/success.txt).
    :param dest_path: Путь к файлу, куда перемещаются ключи для фарминга (например, configs/farm.txt).
    """
    # Убедимся, что ключ не пустой
    key = private_key.strip()
    if not key:
        return

    # Добавляем ключ в dest_path, если его там ещё нет
    if os.path.exists(dest_path):
        with open(dest_path, "r", encoding="utf-8") as dest_file:
            existing_keys = {line.strip() for line in dest_file if line.strip()}
    else:
        existing_keys = set()

    if key not in existing_keys:
        with open(dest_path, "a", encoding="utf-8") as dest_file:
            dest_file.write(key + "\n")
        print(f"Ключ {key} успешно перемещён в {dest_path}")

    # Удаляем ключ из source_path
    if os.path.exists(source_path):
        with open(source_path, "r", encoding="utf-8") as src_file:
            lines = src_file.readlines()
        with open(source_path, "w", encoding="utf-8") as src_file:
            for line in lines:
                if line.strip() != key:
                    src_file.write(line)
