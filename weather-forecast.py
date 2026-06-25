import requests
import time

# ASCII Art untuk title
title = """ 
██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗     ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███████╗████████╗
██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝
██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝    █████╗  ██║   ██║██████╔╝█████╗  ██║     ███████║███████╗   ██║   
██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║     ██╔══██║╚════██║   ██║   
╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║    ██║     ╚██████╔╝██║  ██║███████╗╚██████╗██║  ██║███████║   ██║   
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
""" 

# Function untuk mencari data kota
def find_city(city):
    print(f"Mencari data untuk kota {city}....\n")
    time.sleep(0.5)

    city_response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city}&count=1&language=en&format=json"
        ) # Mengambil dan menyimpan data kota dari API
    
    city_data = city_response.json() # Mengubah format data menjadi dict python

    data = { # Mengekstrak data kota dan ditampung di dalam dict 
        "city_name"      : city_data['results'][0]['name'], # Nama kota
        "city_country"   : city_data['results'][0]['country'], # Negara
        "city_latitude"  : city_data['results'][0]['latitude'], # Koordinat garis lintang
        "city_longitude" : city_data['results'][0]['longitude'], # Koordinat garis bujur
    }

    print(f"[Ditemukan]: {data["city_name"]}, {data["city_country"]}")

    return data # Mengembalikan dict data

# Function untuk mencari data perkiraan cuaca
def get_forecast(city_latitude, city_longitude):
    print("Mencari data cuaca terbaru...\n")
    time.sleep(0.5)

    weather_response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={city_latitude}&longitude={city_longitude}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
        ) # Mengambil dan menyimpan data perkiraan cuaca dari API

    return weather_response.json() # Mengembalikan data perkiraan cuaca dalam bentuk dict

# Function untuk mengambil data perkiraan cuaca
def get_weather_data(city):
    weather_data = get_forecast(
            city_info["city_latitude"],
            city_info["city_longitude"]
        ) # Mengambil nilai lintang bujur kota dengan function get_forecast
    
    data = { # Mengekstrak data perkiraan cuaca dan ditampung di dalam dict
        "date"        : weather_data["current"]["time"][:10], # Hari perkiraan cuaca
        "weather"     : weather_data["current"]["weather_code"], # Perkiraan cuaca dikota
        "temperature" : weather_data["current"]["temperature_2m"], # Temperature di kota
        "wind_speed"  : weather_data["current"]["wind_speed_10m"] # Kecepatan angin dikota
    } 

    return data # Mengembalikan dict data

print(title)
city = input("Masukkan nama kota: ") # Input nama kota

city_info = find_city(city) 

city_weather = get_weather_data(city) # Mengambil data perkiraan cuaca yang sudah disiapkan

print(f"{city_weather["date"]}")
print(f"{city_weather["weather"]}")
print(f"{city_weather["temperature"]} °C")
print(f"{city_weather["wind_speed"]} km/h")