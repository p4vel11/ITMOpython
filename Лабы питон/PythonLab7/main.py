
import sys
import functools
import logging
import requests
import math

def logger(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            use_logging = isinstance(handle, logging.Logger)
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            start_msg = f"INFO: Вызов функции {f.__name__}({signature})\n"
            if use_logging:
                handle.info(start_msg.strip())
            else:
                handle.write(start_msg)

            try:
                result = f(*args, **kwargs)
                end_msg = f"INFO: Функция {f.__name__} завершилась успешно. Результат: {repr(result)}\n"
                if use_logging:
                    handle.info(end_msg.strip())
                else:
                    handle.write(end_msg)
                return result
            except Exception as e:
                error_msg = f"ERROR: Ошибка в функции {f.__name__}: {type(e).__name__}: {str(e)}\n"
                if use_logging:
                    handle.error(error_msg.strip())
                else:
                    handle.write(error_msg)
                raise
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def get_currencies(currency_codes: list, url="https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Не удалось подключиться к API: {e}")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    if "Valute" not in data:
        raise KeyError("Ответ не содержит ключа 'Valute'")

    valute = data["Valute"]
    result = {}

    for code in currency_codes:
        if code not in valute:
            raise KeyError(f"Валюта {code} отсутствует в данных")
        currency_info = valute[code]
        if "Value" not in currency_info:
            raise KeyError(f"Для валюты {code} отсутствует курс")
        value = currency_info["Value"]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты {code} имеет некорректный тип: {type(value)}")
        result[code] = float(value)

    return result


@logger(handle=sys.stdout)
def solve_quadratic(a, b, c):
    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise TypeError("Коэффициенты должны быть числами")

    if a == 0:
        if b == 0:
            raise ValueError("Уравнение не имеет смысла: a = b = 0")
        else:
            root = -c / b
            return (root,)

    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return (root1, root2)
    elif discriminant == 0:
        root = -b / (2 * a)
        return (root,)
    else:
        return ()


if __name__ == "__main__":
    print("=== Демо: solve_quadratic ===")
    solve_quadratic(1, -5, 6)

    print("\n=== Демо: логирование ошибки ===")
    try:
        solve_quadratic(1, 2, 3)
    except:
        pass

    print("\n=== Демо: файловое логирование ===")
    file_logger = logging.getLogger("currency_file")
    file_logger.setLevel(logging.INFO)

    if not file_logger.handlers:
        handler = logging.FileHandler("currency.log", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        file_logger.addHandler(handler)

    get_currencies_logged = logger(handle=file_logger)(get_currencies)
    try:
        result = get_currencies_logged(["USD", "EUR"])
        print("Успех:", result)
    except Exception as e:
        print("Ошибка при получении валют:", e)