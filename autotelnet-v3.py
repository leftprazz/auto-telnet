import requests
import json
from urllib.parse import urlparse
from requests.exceptions import ConnectionError
import time

# Fungsi untuk mendapatkan masukan dari pengguna
def get_user_input():
    raw_url = input("Masukkan URL: ").strip()

    # Menambahkan protokol HTTP jika belum ada
    if not raw_url.startswith(('http://', 'https://')):
        protocol_choice = input("Pilih protokol sesuai nomor (1. HTTP / 2. HTTPS): ").strip()
        if protocol_choice == '1':
            raw_url = 'http://' + raw_url
        elif protocol_choice == '2':
            raw_url = 'https://' + raw_url
        else:
            print("Pilihan protokol tidak valid. Menggunakan HTTPS sebagai default.")
            raw_url = 'https://' + raw_url

    url = raw_url
    method_choice = input("Pilih Metode sesuai nomor (1. GET / 2. POST / 3. PUT / 4. DELETE ): ").strip()
    
    # Mengecek pilihan metode yang dimasukkan oleh pengguna
    if method_choice == '1':
        method = 'GET'
    elif method_choice == '2':
        method = 'POST'
    elif method_choice == '3':
        method = 'PUT'
    elif method_choice == '4':
        method = 'DELETE'
    else:
        print("Pilihan metode tidak valid. Menggunakan GET sebagai default.")
        method = 'GET'

    headers = input("Masukkan Headers (opsional, contoh: 'key:value,key2:value2'): ").strip()

    # Input body dalam bentuk Python dictionary
    print("Masukkan Body (opsional, untuk metode POST/PUT, dll.): ")
    print("Contoh JSON Body: {'key': 'value', 'key2': 'value2'}")
    print("Gunakan tanda kutip (') untuk string di dalam JSON.")
    body_input = input("JSON Body: ").strip()

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
