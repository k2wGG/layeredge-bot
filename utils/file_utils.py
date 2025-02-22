import json
from configs.constants import REGISTER_PATH, FARM_PATH, WALLETS_TO_REFS_PATH, PROXIES_PATH, REFS_PATH
from configs.constants import FAILED_PATH, SUCCESS_PATH, ACCS_REFS_PATH

def read_json(path: str, encoding: str | None = None) -> list | dict:
    with open(path, encoding=encoding) as f:
        return json.load(f)

def read_file(path: str):
    with open(path, encoding='utf-8') as file:
        # Возвращаем только непустые строки
        return [line.strip() for line in file if line.strip()]

def read_farm() -> list[str]:
    return read_file(FARM_PATH)

def read_register() -> list[str]:
    return read_file(REGISTER_PATH)

def read_proxies() -> list[str]:
    return read_file(PROXIES_PATH)

def read_refs_codes() -> list[str]:
    return read_file(REFS_PATH)

def read_wallets_to_get_refs() -> list[str]:
    return read_file(WALLETS_TO_REFS_PATH)

def write_failed_account(private_key: str):
    with open(FAILED_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{private_key}\n')

def write_success_account(private_key: str):
    with open(SUCCESS_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{private_key}\n')

def write_ref_codes(ref_code: str):
    with open(ACCS_REFS_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{ref_code}\n')
