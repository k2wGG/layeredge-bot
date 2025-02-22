import asyncio
import time
from random import random, choice

import aiohttp
from aiohttp import ClientHttpProxyError, ClientResponseError
from eth_account.messages import encode_defunct

from core.account import Account
from utils.file_utils import write_success_account, write_failed_account
from utils.file_utils import read_proxies
from configs.config import SSL
from utils.log_utils import logger
from fake_useragent import UserAgent
from core import db


base_headers = {
    'Accept': "application/json, text/plain, */*",
    'Origin': "https://dashboard.layeredge.io",
}

ua = UserAgent(os=["Windows", "Linux", "Ubuntu", "Mac OS X"])

BAD_PROXIES = []


async def make_request(
method: str,
url: str,
proxy: str,
user_agent: str,
payload: dict = None,
wallet_address: str = "",
retries = 10,
timeout: int = 10
):
    headers = base_headers.copy()
    headers['User-Agent'] = user_agent

    method = method.upper()
    if method == 'POST':
        headers['Content-Type'] = 'application/json'

    for _ in range(retries):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, json=payload, headers=headers, proxy=proxy, timeout=timeout, ssl=SSL) as response:
                    response_json = await response.json()
                    status = response.status
                    response.raise_for_status()
                    return status, response_json
            except ClientHttpProxyError:
                logger.error(f"{wallet_address} | Bad proxy: {proxy}")
                # Если это не последняя попытка, меняем прокси
                if _ + 1 < retries:
                    proxies = read_proxies()
                    proxy = choice(proxies[int(len(proxies)/1.5):])
                    logger.error(f"{wallet_address} | Changed proxy: {proxy}")
                else:
                    return 400, {}

            except ClientResponseError:
                try:
                    return status, response_json
                except:
                    logger.error(f"{wallet_address} | request failed, attempt {_ + 1}/{retries}")
                    await asyncio.sleep(3, 10)
                    if _ + 1 == retries:
                        return 400, {}
            except TimeoutError:
                logger.error(f"{wallet_address} | TimeoutError, attempt {_+1}/{retries}")
                await asyncio.sleep(3, 10)
                if _+1 == retries:
                    return 400, {}
            except Exception as e:
                logger.error(f"{wallet_address} | Unexpected error: {e}, attempt {_+1}/{retries}")
                await asyncio.sleep(3, 10)
                if _+1 == retries:
                    return 400, {}



async def register_wallet(
private_key: str,
wallet_address: str,
proxy: str,
ref_code: str
) -> bool:
    register_data = {
        'walletAddress': wallet_address
    }

    user_agent = ua.random
    response_status, response_json = await make_request(
        'POST',
        f"https://referralapi.layeredge.io/api/referral/register-wallet/{ref_code}",
        proxy,
        user_agent,
        register_data,
        wallet_address,
        retries=20
    )

    if response_status < 300:
        write_success_account(private_key)
        await db.add_account(wallet_address, user_agent)
        logger.success(f"{wallet_address} | Successfully register account")
        return True
    else:
        write_failed_account(private_key)
        if 'message' in response_json:
            if response_json['message'] == "wallet address already registered":
                logger.success(f"{wallet_address} | Wallet already registered, starting farm..")
                return True
            elif response_json['message'] == "invalid invite code":
                logger.error(f"{wallet_address} | Invalid invite code: {ref_code}")
        else:
            logger.error(f"{wallet_address} | Unexpected error: {response_json}")
        return False

async def get_node_status(
account: Account,
proxy: str
):
    url = f"https://referralapi.layeredge.io/api/light-node/node-status/{account.wallet_address}"

    response_status, response_json = await make_request(
        'GET',
        url,
        proxy,
        account.ua,
        wallet_address=account.wallet_address
    )

    if response_status < 300:
        return response_json['data']['startTimestamp']

async def get_points(
account: Account,
proxy: str
) -> int | None:
    url = f"https://referralapi.layeredge.io/api/referral/wallet-details/{account.wallet_address}"

    response_status, response_json = await make_request(
        'GET',
        url,
        proxy,
        account.ua,
        wallet_address=account.wallet_address
    )

    if response_status < 300:
        return response_json['data']["nodePoints"]
    else:
        return None

async def get_ref_code(
account: Account,
proxy: str
) -> str | None:
    url = f"https://referralapi.layeredge.io/api/referral/wallet-details/{account.wallet_address}"

    response_status, response_json = await make_request(
        'GET',
        url,
        proxy,
        account.ua,
        wallet_address=account.wallet_address
    )

    if response_status < 300:
        return response_json['data']["referralCode"]
    else:
        return None

async def start_node(account: Account, proxy):
    timestamp = int(time.time() * 1000)
    message = f"Node activation request for {account.wallet_address} at {timestamp}"
    msghash = encode_defunct(text=message)
    sign = account.evm_account.sign_message(msghash)['signature'].hex()
    data_start = {
        'sign': f"0x{sign}",
        'timestamp': timestamp,
    }

    response_status, response_json = await make_request(
        'POST',
        f"https://referralapi.layeredge.io/api/light-node/node-action/{account.wallet_address}/start",
        proxy,
        account.ua,
        data_start,
        account.wallet_address
    )

    if response_status < 400:
        logger.success(f"{account.wallet_address} | Successfully start node")
        return True
    else:
        if response_status == 405:
            if 'message' in response_json:
                if 'multiple light node' in response_json['message']:
                    logger.warning(f"{account.wallet_address} | Node is already working")
            else:
                logger.error(f"{account.wallet_address} | Error when starting node")
        return False

async def stop_node(account: Account, proxy):
    timestamp = int(time.time() * 1000)
    message = f"Node deactivation request for {account.wallet_address} at {timestamp}"
    msghash = encode_defunct(text=message)
    sign = account.evm_account.sign_message(msghash)['signature'].hex()

    data_stop = {
        'sign': f"0x{sign}",
        'timestamp': timestamp,
    }

    response_status, response_json = await make_request(
        'POST',
        f"https://referralapi.layeredge.io/api/light-node/node-action/{account.wallet_address}/stop",
        proxy,
        account.ua,
        data_stop,
        account.wallet_address
    )

    if response_status < 400:
        logger.success(f"{account.wallet_address} | Successfully stop node")
        return True
    else:
        if response_status == 404:
            if 'message' in response_json:
                if 'no node running' in response_json['message']:
                    # node is not running
                    pass
                    # logger.warning(f"{account.wallet_address} | Node is not running")
            else:
                logger.error(f"{account.wallet_address} | Error when stopping node")
        return False

async def check_in(account: Account, proxy):
    timestamp = int(time.time() * 1000)
    message = f"I am claiming my daily node point for {account.wallet_address} at {timestamp}"
    msghash = encode_defunct(text=message)
    sign = account.evm_account.sign_message(msghash)['signature'].hex()

    data_check_in = {
        'sign': f"0x{sign}",
        'timestamp': timestamp,
        'walletAddress': account.wallet_address,
    }

    response_status, response_json = await make_request(
        'POST',
        f"https://referralapi.layeredge.io/api/light-node/claim-node-points",
        proxy,
        account.ua,
        data_check_in,
        account.wallet_address
    )

    if response_status < 400:
        logger.success(f"{account.wallet_address} | Successfully claim daily check in")
        return True
    else:
        if response_status == 405:
            if 'message' in response_json:
                if '24 hours' in response_json['message']:
                    logger.warning(f"{account.wallet_address} | Check in is already done")
            else:
                logger.error(f"{account.wallet_address} | Failed to perform check in")
        return False
