import requests
import datetime

# URL и заголовки API
url = "https://sky-scanner3.p.rapidapi.com/flights/cheapest-one-way"
headers = {
    "x-rapidapi-key": "9f6ddf44e8mshdb360170e8bb649p1184e1jsnbab8a28969d7",  # Замените вашим ключом API
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
    "Content-Type": "application/json"
}

def validate_date(date_text):
    """Проверка корректности формата даты."""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_cheapest_flights(origin, destination, date):
    """Запрос данных о самых дешевых авиабилетах."""
    payload = {
        "origin": origin,
        "destination": destination,
        "date": date,
        "adults": 1,
        "currency": "USD"  # Укажите предпочитаемую валюту
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        flights = response.json().get("data", [])

        if not flights:
            print("\nНет доступных рейсов.")
            return

        # Сортировка рейсов по цене и выбор топ-5
        cheapest_flights = sorted(flights, key=lambda x: x['price'])[:5]

        print("\nТоп-5 самых дешевых рейсов:")
        for idx, flight in enumerate(cheapest_flights, start=1):
            print(f"{idx}. Цена: {flight['price']} {flight['currency']}, Дата: {flight['date']}")

    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при обращении к API:", e)
    except KeyError:
        print("Неправильный формат ответа от API.")

def main():
    print("Добро пожаловать в поиск дешевых авиабилетов!")

    # Ввод городов отправления и прибытия
    origin = input("Введите город отправления (IATA-код): ")
    destination = input("Введите город прибытия (IATA-код): ")

    # Ввод и проверка даты
    while True:
        date = input("Введите дату отправления (в формате yyyy-mm-dd): ")
        if validate_date(date):
            break
        print("Некорректный формат даты. Попробуйте снова.")

    get_cheapest_flights(origin, destination, date)

if __name__ == "__main__":
    main()
