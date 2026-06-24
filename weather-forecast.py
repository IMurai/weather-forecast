import requests
import time

title = """
██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗     ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███████╗████████╗
██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝
██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝    █████╗  ██║   ██║██████╔╝█████╗  ██║     ███████║███████╗   ██║   
██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║     ██╔══██║╚════██║   ██║   
╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║    ██║     ╚██████╔╝██║  ██║███████╗╚██████╗██║  ██║███████║   ██║   
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
"""

city = input("Masukkan nama kota: ")

print(f"Mencari data untuk kota {city}....\n")
time.sleep(0.5)

city_response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json")
city_data = city_response.json()

city_name = city_data['results'][0]['name']
city_province = city_data['results'][0]['admin1']

print(f"[Ditemukan]: {city_name}, {city_province}")
print("Mencari data cuaca terbaru...\n")
time.sleep(0.5)

city_latitude = city_data['results'][0]['latitude']
city_longitude = city_data['results'][0]['longitude']

weather_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city_latitude}&longitude={city_longitude}&current=temperature_2m,weather_code,wind_speed_10m")
weather_data = weather_response.json()

date = weather_data["current"]["time"][:10]
weather = weather_data["current"]["weather_code"]
temperature = weather_data["current"]["temperature_2m"]
wind_speed = weather_data["current"]["wind_speed_10m"]

print(f"{city_name}, {city_province} {date}")
print(weather)
print(f"{temperature} °C")
print(f"{wind_speed} km/h")