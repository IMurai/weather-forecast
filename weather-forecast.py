import requests
import time

# =================================================
# ASCII Art untuk title
# =================================================
title = """ 
██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗     ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███████╗████████╗
██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝
██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝    █████╗  ██║   ██║██████╔╝█████╗  ██║     ███████║███████╗   ██║   
██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║     ██╔══██║╚════██║   ██║   
╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║    ██║     ╚██████╔╝██║  ██║███████╗╚██████╗██║  ██║███████║   ██║   
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
""" 

# =================================================
# Function untuk mencari data kota
# =================================================
def find_city(city):
    print(f"Mencari data untuk kota '{city}'....\n")
    time.sleep(0.5)

    city_response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city}&count=1&language=en&format=json"
        ) # Mengambil dan menyimpan data kota dari API
    
    city_data = city_response.json() # Mengubah format data menjadi dict python

    data = { # Mengekstrak data kota dan ditampung di dalam dict 
        "name"      : city_data['results'][0]['name'],      # Nama kota
        "country"   : city_data['results'][0]['country'],   # Negara
        "latitude"  : city_data['results'][0]['latitude'],  # Koordinat garis lintang
        "longitude" : city_data['results'][0]['longitude'], # Koordinat garis bujur
    }

    print(f"[Ditemukan]: {data["name"]}, {data["country"]}")

    return data # Mengembalikan dict data

# =================================================
# Function untuk mencari data perkiraan cuaca
# =================================================
def get_forecast(latitude, longitude):
    print("Mengambil data cuaca terbaru...\n")
    time.sleep(0.5)

    weather_response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
        ) # Mengambil dan menyimpan data perkiraan cuaca dari API

    return weather_response.json() # Mengembalikan data perkiraan cuaca dalam bentuk dict

# =================================================
# Function untuk mengambil data perkiraan cuaca
# =================================================
def get_weather_data():
    weather_data = get_forecast(
            city_info["latitude"],
            city_info["longitude"]
        ) # Mengambil nilai lintang bujur kota dengan function get_forecast
    
    data = { # Mengekstrak data perkiraan cuaca dan ditampung di dalam dict
        "date"         : weather_data["current"]["time"][:10],      # Tanggal pemantauan cuaca (YYYY-MM-DD)
        "time"         : weather_data["current"]["time"][11:],      # Waktu pemantauan cuaca
        "temperature"  : weather_data["current"]["temperature_2m"], # Suhu (°C)
        "wind_speed"   : weather_data["current"]["wind_speed_10m"]  # Kecepatan angin (km/h)
    } 

    return data # Mengembalikan dict data

# =================================================
    "PROGRAM UTAMA"
# =================================================
session = 0

print(title)

while True:
    if session == 0:
        quit_massage = ""
    else:
        quit_massage = "(Ketik 'quit' untuk berhenti)"

    city = input(f"\nMasukkan nama kota{quit_massage}: ") # Input nama kota

    if city == "quit":
        break

    city_info = find_city(city) 

    city_weather = get_weather_data() # Mengambil data perkiraan cuaca yang sudah disiapkan

    print(f"{city_info["name"]}, {city_info["country"]}\n")

    print(f"- Waktu pantau    : {city_weather["date"]} {city_weather["time"]}")
    print(f"- Kondisi cuaca   : {city_weather["weather"]}")
    print(f"- Suhu            : {city_weather["temperature"]} °C")
    print(f"- Kecepatan angin : {city_weather["wind_speed"]} km/h")

    session += 1