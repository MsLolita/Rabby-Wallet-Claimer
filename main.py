import random
import time

from utils import Web3Utils, file_to_list, logger
from inputs.config import BONUS_CODE, DELAY
from fake_useragent import UserAgent

import requests

url = "https://api.rabby.io/v1/points/claim_snapshot"

headers = {
    "Host": "api.rabby.io",
    "Connection": "keep-alive",
    "Content-Length": "224",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "X-Version": "0.92.48",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": UserAgent().random,
    "x-api-ts": "1706015066",
    "Content-Type": "application/json",
    "x-api-ver": "v2",
    "Accept": "application/json, text/plain, */*",
    "X-Client": "Rabby",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
}


wallets = file_to_list("inputs/wallets.txt")
proxies = file_to_list("inputs/proxies.txt")


for raw_wallet in wallets:
    try:
        if " " in raw_wallet.strip():
            client = Web3Utils(mnemonic=raw_wallet)
        else:
            client = Web3Utils(key=raw_wallet)

        address = client.acct.address.lower()
        msg = f"{address} Claims Rabby Points"

        payload = {
            "id": address,
            "signature": client.get_signed_code(msg),
            "invite_code": BONUS_CODE
        }

        response = requests.post(url, headers=headers, json=payload, proxies={"http": f"http://{proxies[0]}"})

        if response.json().get("error_code") == 0:
            resp_msg = "Claimed!"
            logger.success(f"{address} | Claimed!")
        else:
            resp_msg = response.json().get("error_msg")
            logger.info(f"{address} | {resp_msg}")

        time.sleep(random.uniform(*DELAY))
    except Exception as e:
        logger.error(f"{raw_wallet[:15]}... | {e}")
