import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

LOG_DIR = os.path.join(ROOT_DIR, "log")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
CONFIGS_DIR = os.path.join(ROOT_DIR, "configs")
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Создаём необходимые директории, если они не существуют
for directory in (LOG_DIR, RESULTS_DIR, CONFIGS_DIR, DATA_DIR):
    if not os.path.exists(directory):
        os.makedirs(directory)

FAILED_PATH = os.path.join(RESULTS_DIR, 'failed.txt')
SUCCESS_PATH = os.path.join(RESULTS_DIR, 'success.txt')
ACCS_REFS_PATH = os.path.join(RESULTS_DIR, 'accounts_refs.txt')
DATABASE_PATH = os.path.join(DATA_DIR, 'data.db')
LOG_PATH = os.path.join(LOG_DIR, 'log.log')
REFS_PATH = os.path.join(CONFIGS_DIR, "REFS.txt")
FARM_PATH = os.path.join(CONFIGS_DIR, "farm.txt")
REGISTER_PATH = os.path.join(CONFIGS_DIR, "register.txt")
PROXIES_PATH = os.path.join(CONFIGS_DIR, "proxies.txt")
WALLETS_TO_REFS_PATH = os.path.join(CONFIGS_DIR, "get_refs.txt")
