import requests
from typing import Union


class Crpt:
    def __init__(self, proxy: str | None = None):
        self.proxy = proxy

    def _post(self, data: Union[dict, list]) -> Union[list, dict]:
        return requests.post(
            f"https://mobile.api.crpt.ru/mobile/check",
            json=data,
            headers={
                "content-type": "application/json",
                "accept": "application/json",
                "user-agent": "Platform: iOS 17.2; AppVersion: 4.47.0; AppVersionCode: 7630; Device: iPhone 14 Pro;",
                "client": "iOS 17.2; AppVersion: 4.47.0; Device: iPhone 14 Pro;",
            },
            proxies={
                "http": self.proxy,
                "https": self.proxy
            },
        ).json()

    def infoFromReceipt(self, code: str) -> Union[list, dict]:
        return self._post(
            {
                "code": code,
                "codeType": "qr",
            }
        )
