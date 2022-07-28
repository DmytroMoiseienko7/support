import json

import requests
from django.http import JsonResponse


class ExchangeRate:
    def __init__(self, from_: str, to_: str, value: float) -> None:
        self.from_: str = from_
        self.to_: str = to_
        self.value: float = value

    @classmethod
    def from_response(cls, response: dict):
        pure_response: dict = response["Realtime Currency Exchange Rate"]
        value = pure_response["5. Exchange Rate"]
        from_ = pure_response["1. From_Currency Code"]
        to_ = pure_response["3. To_Currency Code"]

        return cls(value=value, from_=from_, to_=to_)

    def as_dict(self):
        return {
            "from": self.from_,
            "to": self.to_,
            "value": self.value,
        }

    def __eq__(self, other: "ExchangeRate") -> bool:
        return self.value == other.value


class JsonMemoryFile:
    HISTORY_JSON_FILE = "config/memory_files/history.json"

    @classmethod
    def read_json_file(cls):
        with open(cls.HISTORY_JSON_FILE, "r") as file:
            data = json.load(file)
        return data

    @classmethod
    def write_to_json(cls, data):
        with open(cls.HISTORY_JSON_FILE, "w") as file:
            json.dump(data, file)


class ExchangeRateHistory:

    _history = []

    @classmethod
    def add(cls, instance) -> None:
        if not cls._history:
            cls._history.append(instance)
        elif cls._history[-1] != instance:
            cls._history.append(instance)

    @classmethod
    def as_dict(cls) -> list:
        return {"results": [er.as_dict() for er in cls._history]}


def btc_usd(request):
    # NOTE Connect to exchange rates API
    API_key = "KP5A01WINLXSTYUY"
    firtst_url_part = "https://www.alphavantage.co/query?function="
    url = f"{firtst_url_part}CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={API_key}"
    response = requests.get(url)

    # NOTE Parse the source response
    exchange_rate = ExchangeRate.from_response(response.json())

    # NOTE Add result to the exchange rate history

    ExchangeRateHistory.add(exchange_rate)

    JsonMemoryFile.write_to_json(ExchangeRateHistory.as_dict())

    return JsonResponse(exchange_rate.as_dict())


def history(request):
    return JsonResponse(JsonMemoryFile.read_json_file())


def home(request):
    data = {"message": "Hello World"}
    return JsonResponse(data)
