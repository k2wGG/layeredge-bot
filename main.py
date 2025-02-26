import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

from utils.Console import Console
from core import register, farm, db
from get_refs import start as get_refs_start
from utils.log_utils import logger
from configs import config

def print_menu():
    print()
    print("=== LayerEdge Interactive Menu ===")
    print("1) Запустить регистрацию аккаунтов")
    print("2) Запустить фарм 24/7")
    print("3) Получить реферальные коды")
    print("4) Настроить скрипт")
    print("0) Выход")
    return input("Ваш выбор: ").strip()

def configure_project():
    """
    Простая функция для интерактивной настройки проекта:
    - REGISTER_MODE (режим регистрации)
    - FARM_MODE (режим фарма)
    - MIN_DELAY_BEFORE_START
    - MAX_DELAY_BEFORE_START
    """
    print("\n=== Настройка проекта ===")
    
    reg_input = input(f"Включить режим регистрации? (True/False) [Текущее значение: {config.REGISTER_MODE}]: ").strip()
    farm_input = input(f"Включить режим фарма 24/7? (True/False) [Текущее значение: {config.FARM_MODE}]: ").strip()
    
    try:
        if reg_input:
            config.REGISTER_MODE = (reg_input.lower() == "true")
        if farm_input:
            config.FARM_MODE = (farm_input.lower() == "true")
    except Exception as e:
        print("Ошибка при вводе режима:", e)

    print("\n=== Настройка задержек перед стартом аккаунта ===")
    min_delay_input = input(f"Минимальная задержка (в секундах) [Текущее значение: {config.MIN_DELAY_BEFORE_START}]: ").strip()
    max_delay_input = input(f"Максимальная задержка (в секундах) [Текущее значение: {config.MAX_DELAY_BEFORE_START}]: ").strip()
    
    try:
        if min_delay_input:
            config.MIN_DELAY_BEFORE_START = int(min_delay_input)
        if max_delay_input:
            config.MAX_DELAY_BEFORE_START = int(max_delay_input)
    except Exception as e:
        print("Ошибка при вводе задержек:", e)

    print("Настройки успешно обновлены.\n")

async def main():
    # Показываем ASCII-баннер
    Console().build()

    # Создаём/проверяем базу данных
    await db.create_database()

    while True:
        choice = print_menu()
        if choice == '1':
            # Режим регистрации аккаунтов
            await register.start()
        elif choice == '2':
            # Режим фарма 24/7
            await farm.start()
        elif choice == '3':
            # Получить реферальные коды
            await get_refs_start()
        elif choice == '4':
            # Настройка проекта (режимы и задержки)
            configure_project()
        elif choice == '0':
            logger.info("Выход из приложения...")
            sys.exit(0)
        else:
            print("Неверный выбор. Повторите снова.")

if __name__ == "__main__":
    asyncio.run(main())
