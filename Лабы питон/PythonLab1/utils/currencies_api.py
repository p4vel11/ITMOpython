import requests
from xml.etree import ElementTree as ET
from models.currency import Currency

def get_currencies() -> list[Currency]:
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    response.raise_for_status()
    root = ET.fromstring(response.content)

    currencies = []
    for valute in root.findall("Valute"):
        id_ = valute.get("ID")
        num_code = valute.find("NumCode").text
        char_code = valute.find("CharCode").text
        nominal = int(valute.find("Nominal").text)
        name = valute.find("Name").text
        value_str = valute.find("Value").text.replace(",", ".")
        value = float(value_str)

        currency = Currency(
            id_=id_,
            num_code=num_code,
            char_code=char_code,
            name=name,
            value=value,
            nominal=nominal
        )
        currencies.append(currency)

    return currencies