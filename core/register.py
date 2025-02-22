from utils.log_utils import logger
from utils.file_utils import read_register, read_refs_codes, read_proxies
from utils.private_key_to_wallet import private_key_to_wallet
from random import choice
from core.reqs import register_wallet
from utils.total_time_to_register import get_random_delay
from utils.move_account import move_account_to_farm  # Импорт функции перемещения
from configs.constants import SUCCESS_PATH, FARM_PATH      # Пути для файлов: например, results/success.txt и configs/farm.txt
import asyncio
from core.farm import process_account

PRIVATE_KEYS_TO_REG = read_register()
REFS = read_refs_codes()
PROXIES = read_proxies()
TOTAL_WALLETS = len(PRIVATE_KEYS_TO_REG)

async def start():
    for i, data in enumerate(zip(PRIVATE_KEYS_TO_REG, PROXIES)):
        private_key, proxy = data[0], data[1]
        wallet_address = private_key_to_wallet(private_key)
        logger.info(f"{wallet_address} | Starting to register an account..")
        registered = await register_wallet(private_key, wallet_address, proxy, choice(REFS))
        if registered:
            logger.success(f"{wallet_address} | Successfully register account")
            # Перемещаем ключ из файла с успешными регистрациями в файл для фарма
            move_account_to_farm(private_key, SUCCESS_PATH, FARM_PATH)
            # Запускаем фарминг для аккаунта
            asyncio.create_task(process_account(private_key, proxy))
        if i != TOTAL_WALLETS - 1:
            await asyncio.sleep(get_random_delay(TOTAL_WALLETS) / 2)
    await asyncio.sleep(float("inf"))

if __name__ == '__main__':
    asyncio.run(start())
