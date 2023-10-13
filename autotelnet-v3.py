import requests
import json
from urllib.parse import urlparse
from requests.exceptions import ConnectionError
import time

# Fungsi untuk mendapatkan masukan dari pengguna
def get_user_input():
    url = input("Masukkan URL: ")
    method = input("Pilih Metode HTTP (GET/POST/PUT/DELETE, dll.): ").upper()
    headers = input("Masukkan Headers (opsional, contoh: 'key:value,key2:value2'): ").strip()

    # Input body dalam bentuk Python dictionary
    body_input = input("Masukkan Body (opsional, untuk metode POST/PUT, dll.): ").strip()

    # Mengonversi input body ke bentuk dictionary
    try:
        body = json.loads(body_input)
    except json.JSONDecodeError:
        print("Format JSON tidak valid.")
        return None, None, None, None

    return url, method, headers, body

def main():
    while True:
        url, method, headers, body = get_user_input()

        if body is None:
            return

        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            print("URL tidak valid atau tidak menggunakan protokol HTTP atau HTTPS.")
            return

        print("------------------------------")

        start_time = time.time()  # Waktu awal sebelum mengirim request

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=json.loads(headers) if headers else {}, timeout=3600)
            elif method == "POST":
                # Menggunakan json.dumps untuk mengonversi dictionary body ke JSON string yang valid
                response = requests.post(url, headers=json.loads(headers) if headers else {}, json=body, timeout=3600)

            end_time = time.time()  # Waktu setelah menerima response
            total_time = end_time - start_time  # Menghitung total waktu

            print("Response dari endpoint:")
            print(f"HTTP Status Code: {response.status_code}")
            print(response.text)
            print(f"Total waktu yang dibutuhkan: {total_time:.2f} detik")

        except ConnectionError as e:
            print(f"Tidak mendapatkan respon dari endpoint (Error: {e})")
        except requests.Timeout:
            print("Tidak mendapatkan respons dari endpoint (Timeout)")

        print("------------------------------")

        print("Detail endpoint:")
        print(f"URL: {url}")

        # Meminta input dari pengguna untuk menentukan apakah ingin menjalankan program lagi atau tidak
        ulangi = input("Apakah Anda ingin menjalankan program lagi? (ya/tidak): ").lower()
        if ulangi != 'ya':
            break

if __name__ == "__main__":
    main()
