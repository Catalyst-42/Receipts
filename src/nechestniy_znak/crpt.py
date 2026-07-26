"""
Note: this file is a copy of original source just with some tweaks to add a proxy

Original source: https://github.com/li0ard/nechestniy_znak
Original author: https://github.com/li0ard
"""

import requests
from typing import Union


class Crpt:
    def __init__(self, proxy: str | None = None):
        self.proxy = None

        if proxy is not None:
            self.proxy = {"http": proxy, "https": proxy}

    def _post(self, data: Union[dict, list]) -> Union[list, dict]:
        result = requests.post(
            f"https://mobile.api.crpt.ru/mobile/check",
            json=data,
            headers={
                "content-type": "application/json",
                "accept": "application/json",
                "user-agent": "Platform: iOS 17.2; AppVersion: 4.47.0; AppVersionCode: 7630; Device: iPhone 14 Pro;",
                "client": "iOS 17.2; AppVersion: 4.47.0; Device: iPhone 14 Pro;",
            },
            proxies=self.proxy,
        )

        result.raise_for_status()
        return result.json()

    def infoFromReceipt(self, code: str) -> Union[list, dict]:
        return self._post(
            {
                "code": code,
                "codeType": "qr",
            }
        )
