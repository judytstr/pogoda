import requests
from datetime import datetime, timedelta

def check_rainfall(date):
    latitude = "54.3520"
    longitude = "18.6466"
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FWarsaw&start_date={date}&end_date={date}"

    try:
        response = requests.get(api_url)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Response data:", data)

            if 'hourly' in data and 'rain' in data['hourly']:
                hourly_rain = data['hourly']['rain']

                # Sprawdź, czy występują opady deszczu w danych godzinowych
                if any(rainfall > 0.0 for rainfall in hourly_rain):
                    return "Będzie padać"
                else:
                    return "Nie będzie padać"
            else:
                print("Nie znaleziono danych godzinowych o opadach deszczu.")
                return "Nie wiem"
        else:
            print("Wystąpił problem z zapytaniem do serwera. Status:", response.status_code)
            return "Nie wiem"

    except requests.exceptions.RequestException as e:
        print("Nie udało się pobrać danych z API:", e)
        return "Nie wiem"

def save_to_file(date, result):
    with open("weather_results.txt", "a") as file:
        file.write(f"{date}: {result}\n")

def read_from_file(date):
    try:
        with open("weather_results.txt", "r") as file:
            for line in file:
                if date in line:
                    return line.strip().split(": ")[1]
            return None
    except FileNotFoundError:
        return None

def main():
    date_input = input("Podaj datę w formacie YYYY-mm-dd (jeśli puste, użyję następnego dnia): ")
    if not date_input:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        date = date_input

    result_from_file = read_from_file(date)
    if result_from_file:
        print("Wynik z pliku:", result_from_file)
    else:
        result = check_rainfall(date)
        save_to_file(date, result)
        print("Wynik zapytania:", result)

if __name__ == "__main__":
    main()

