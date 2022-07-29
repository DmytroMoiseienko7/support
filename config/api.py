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


class JsonMemoryFile:
    def __init__(self) -> None:
        self.HISTORY_JSON_FILE = "config/memory_files/history.json"

    def read_json_file(self):
        with open(self.HISTORY_JSON_FILE, "r") as file:
            data = json.load(file)
        return data

    def write_to_json(self, data):
        with open(self.HISTORY_JSON_FILE, "w") as file:
            json.dump(data, file)


class ExchangeRateHistory(JsonMemoryFile):
    def __init__(self, instance) -> None:
        self.instance = instance
        super().__init__()
        self.memory_file = super().read_json_file()["results"]

    def add(self, instance) -> None:
        if not self.memory_file:
            self.memory_file.append(instance)
        elif self.memory_file[-1] != instance:
            self.memory_file.append(instance)

    def as_dict(self) -> dict:
        return {"results": [er for er in self.memory_file]}


def btc_usd(request):
    # NOTE Connect to exchange rates API
    API_key = "KP5A01WINLXSTYUY"
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency=BTC&to_currency=USD&apikey={API_key}"
    )
    response = requests.get(url)

    # NOTE Parse the source response
    exchange_rate = ExchangeRate.from_response(response.json())

    # NOTE Add result to the exchange rate history
    exchange_rate_history = ExchangeRateHistory(exchange_rate)
    exchange_rate_history.add(exchange_rate.as_dict())

    # NOTE Write down exchange rate history to the json file
    json_memory_file = JsonMemoryFile()
    json_memory_file.write_to_json(exchange_rate_history.as_dict())

    return JsonResponse(exchange_rate.as_dict())


def history(request):
    json_memory_file = JsonMemoryFile()
    return JsonResponse(json_memory_file.read_json_file())


def home(request):
    data = {"message": "Hello World"}
    return JsonResponse(data)
