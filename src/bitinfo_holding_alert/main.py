import logging
import sys
from typing import Optional

from bitinfo_holding_alert.config import TRACK_ADDRESS, TRACK_COIN
from bitinfo_holding_alert.scrap import get_wallet_holding_data
from bitinfo_holding_alert.cal import produce_time_series


LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


def bitinfo_holding_ts(
    track_addr: Optional[str] = None,
    track_coin: Optional[str] = None,
    timeframe: Optional[str] = "4h",
    sma: Optional[int] = 20,
):
    """Scrap the data from bitinfo and calculate the balance based on the resample frequency.
    track_addr (str): The address to track.
    track_coin (str): The coin to track.
    timeframe (str): The resample frequency.
    sma (int): The moving average window.

    For example, if the website url is
    https://bitinfocharts.com/dogecoin/address/DRSqEwcnJX3GZWH9Twtwk8D5ewqdJzi13k-full/

    track_coin value would be `dogecoin` and track_addr would be `DRSqEwcnJX3GZWH9Twtwk8D5ewqdJzi13k`.
    
    For timeframe, we support frequency that listed on pandas doc, common value would be '4h', '1h', '1d'
    
    Full list of timeframe available: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    """
    LOGGER.info(f"Scrapping data for {track_coin}, wallet address: {track_addr}")

    track_addr = TRACK_ADDRESS if track_addr is None else track_addr
    track_coin = TRACK_COIN if track_coin is None else track_coin

    df_holding_ts = get_wallet_holding_data(
        coin=track_coin,
        address=track_addr,
    )

    balance_ts = produce_time_series(df_holding_ts, timeframe, sma)

    return balance_ts


if __name__ == "__main__":
    # balance_ts = bitinfo_holding_ts("DRSqEwcnJX3GZWH9Twtwk8D5ewqdJzi13k", "dogecoin", "4h", 20)
    balance_ts = bitinfo_holding_ts("3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys", "bitcoin", "1h", 20)
    print(balance_ts)