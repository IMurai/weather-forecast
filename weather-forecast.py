import requests
import time

# =================================================Z
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
"Function untuk mencari data kota"
# =================================================
def find_city(city):
    print(f"Mencari data untuk kota '{city}'....\n")
    time.sleep(0.5)

    city_response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}" # Mengirim request ke API dengan nama kota sebagai query 
        f"&count=1&language=en" # Mengambil 1 data teratas
        f"&format=json" # Response dalam format json
        ) 
    
    city_data = city_response.json() # Mengubah format data menjadi dict python

    data = { # Mengekstrak data kota dan ditampung di dalam dict 
        "name"      : city_data['results'][0]['name'],      # Nama kota
        "country"   : city_data['results'][0]['country'],   # Negara
        "latitude"  : city_data['results'][0]['latitude'],  # Koordinat garis lintang
        "longitude" : city_data['results'][0]['longitude'], # Koordinat garis bujur
    }

    print(f"[Ditemukan]: {data["name"]}, {data["country"]}")

    return data # Mengembalikan data kota

# =================================================
"Function untuk mencari data perkiraan cuaca"
# =================================================
def get_forecast(latitude, longitude):
    print("Mengambil data cuaca terbaru...\n")
    time.sleep(0.5)

    weather_response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
        ) # Mengambil dan menyimpan data perkiraan cuaca dari API

    return weather_response.json() # Mengembalikan data response(data mentah) dalam bentuk dict

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

    return data # Mengembalikan data perkiraan cuaca

# =================================================
"PROGRAM UTAMA"
# =================================================
session = 0 # Melacak jumlah pencarian yang sudah dilakukan

print(title) # Menampilkan judul program

while True: # Looping utama: berjalan sampai user memilih 'quit'
    quit_massage = ""

    if session > 0: # Tampilkan opsi keluar hanya jika user sudah pernah melakukan pencarian
        quit_massage = "(Ketik 'quit' untuk berhenti)"

    city = input(f"\nMasukkan nama kota{quit_massage}: ") # Input nama kota

    if city == "quit": # Menghentikan loop saat user memilih quit
        break

    city_info = find_city(city) # Mencari data kota berdasarkan input
    city_weather = get_weather_data() # Mengambil data perkiraan cuaca 

    print(f"{city_info["name"]}, {city_info["country"]}\n") # Menampilkan nama kota dan negara

    # Menampilkan detail informasi cuaca secara terformat
    print(f"- Waktu pantau    : {city_weather["date"]} {city_weather["time"]}")
    print(f"- Kondisi cuaca   : {city_weather["weather"]}")
    print(f"- Suhu            : {city_weather["temperature"]} °C")
    print(f"- Kecepatan angin : {city_weather["wind_speed"]} km/h")

    session += 1 # Menambahkan jumlah sesi
