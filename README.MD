# bitinfo holding alert

Scrapping wallet holding data from bitinfo for specific token-wallet pair, timestamp is express in UTC.

# Installation
## Install module

`pip install .`

## Add docker service to bypass Cloudflare protection
Target website has a Cloudflare protection. `FalreSolverr` docker service is required to bypass that. Follow the instruction below to add a docker service in your machine.

On your machine, run

```bash
docker pull flaresolverr/flaresolverr

docker run -d -p 8191:8191 --name=flaresolverr --restart unless-stopped -e LOG_LEVEL=info flaresolverr/flaresolverr
```

localhost port 8191 will by default be used to listen to scrap request.

To bypass cloudflare, the one-line curl post command would be

```bash
curl --location --request POST 'http://localhost:8191/v1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "cmd": "request.get",
    "url":"https://bitinfocharts.com/dogecoin/address/DRSqEwcnJX3GZWH9Twtwk8D5ewqdJzi13k-full/",
    "maxTimeout": 100000
}'
```

You can also checkout the [repo](https://github.com/FlareSolverr/FlareSolverr) or [docker image](https://hub.docker.com/r/flaresolverr/flaresolverr).

## How to use
### Quick Start
```python
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

from bitinfo_holding_alert.main import bitinfo_holding_ts

balance_ts = bitinfo_holding_ts(
    track_addr="DRSqEwcnJX3GZWH9Twtwk8D5ewqdJzi13k",
    track_coin="dogecoin",
    timeframe="4h",
    sma=20
)
```