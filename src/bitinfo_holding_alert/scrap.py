import json
from typing import Optional
import logging

import pandas as pd
import requests

from bitinfo_holding_alert.config import CLOUDFLARE_BYPASS_URL


LOGGER = logging.getLogger(__name__)


def validate_bypass_response(response: json) -> bool:
    if response["status"] != "ok":
        LOGGER.error(f"Error: {response['status']}, please check docker logging")
        LOGGER.error(f"Docker response_json: {response}")
        return False

    return True


def filter_holding_table(dfs: list) -> pd.DataFrame:
    for df in dfs:
        if "Block" in df:
            return df

    return pd.DataFrame()


def get_wallet_holding_data(
    coin: str, 
    address: str,
    bypass_url: Optional[str] = CLOUDFLARE_BYPASS_URL,
    ) -> pd.DataFrame:
    """
    Get the full transaction history for any coin - address pair.
    """
    bitinfo_url = f"https://bitinfocharts.com/{coin}/address/{address}-full/"

    payload = json.dumps({
        "cmd": "request.get",
        "url": bitinfo_url,
        "maxTimeout": 200000
    })

    headers = {
        'Content-Type': 'application/json'
    }

    LOGGER.info(f"Requesting data from docker: {bypass_url}")

    response = requests.request("POST", bypass_url, headers=headers, data=payload)
    response_json = json.loads(response.content)

    if not validate_bypass_response(response_json):
        raise Exception("Cloudflare bypass failed")

    _html = response_json["solution"]["response"]

    dfs = pd.read_html(_html)
    df_holding_ts = filter_holding_table(dfs)

    return df_holding_ts
