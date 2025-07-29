import requests
from PIL import Image
import io

WEATHER_EMOJI = {
    "Sunny": "☀️",
    "Clear": "🌙",
    "Partly": "⛅",
    "Cloudy": "☁️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Thunder": "⛈️",
    "Fog": "🌫️"
}

city = "Moscow"
url = f"http://wttr.in/{city}?format=j1"

try:
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    
    current_condition = weather_data['current_condition'][0]
    temp = current_condition['temp_C']
    feels_like = current_condition['FeelsLikeC']
    description = current_condition['weatherDesc'][0]['value']
    
    # Иконка
    icon_url = current_condition['weatherIconUrl'][0]['value']
    emoji = WEATHER_EMOJI.get(description.split()[0], "🌈")
    
    if icon_url and icon_url.startswith('http'):
        print(f"URL иконки: {icon_url}")
        try:
            icon_response = requests.get(icon_url)
            img = Image.open(io.BytesIO(icon_response.content))
            img.show()
        except:
            print(f"Не удалось загрузить иконку, используем эмодзи: {emoji}")
    else:
        print(f"Иконка недоступна, используем эмодзи: {emoji}")
    
    print(f"\nСейчас в {city}: {temp}°C {emoji}")
    print(f"Ощущается как: {feels_like}°C")
    print(f"Описание: {description}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {e}")
except KeyError as e:
    print(f"Ошибка в структуре данных: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")