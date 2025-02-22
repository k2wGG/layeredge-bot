from web3 import AsyncWeb3
w3 = AsyncWeb3()

def private_key_to_wallet(private_key: str):
    pk = private_key.strip()  # Убираем пробелы
    if not pk:
        raise ValueError("Empty private key provided")
    # Добавляем "0x", если его нет
    if not pk.startswith("0x"):
        pk = "0x" + pk
    return w3.eth.account.from_key(pk).address
