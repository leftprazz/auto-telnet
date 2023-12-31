import requests
import json
from urllib.parse import urlparse
from requests.exceptions import ConnectionError
import time

def get_user_input(previous_body=None):
    raw_url = input("Masukkan URL: ").strip()

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

    if previous_body:
        print(f"Body Sebelumnya: {json.dumps(previous_body, indent=4)}")
        modify_body = input("Apakah Anda ingin memodifikasi body sebelumnya? (ya/tidak): ").lower()
        if modify_body == 'ya':
            body = get_modified_body(previous_body)
        else:
            body = previous_body
    else:
        print("Masukkan Body (opsional, untuk metode POST/PUT, dll.): ")
        print("Contoh JSON Body: {'key': 'value', 'key2': 'value2'}")
        print("Gunakan tanda kutip (') untuk string di dalam JSON.")
        body_input = input("JSON Body: ").strip()

        try:
            body = json.loads(body_input)
        except json.JSONDecodeError:
            print("Format JSON tidak valid.")
            return None, None, None, None

    return url, method, headers, body

def get_modified_body(previous_body):
    print("Masukkan Body yang Dimodifikasi:")
    print("Contoh JSON Body: {'key': 'value', 'key2': 'value2'}")
    print("Gunakan tanda kutip (') untuk string di dalam JSON.")
    modified_body_input = input("JSON Body: ").strip()

    try:
        modified_body = json.loads(modified_body_input)
    except json.JSONDecodeError:
        print("Format JSON tidak valid.")
        return get_modified_body(previous_body)

    return modified_body

def main():
    previous_url = None
    previous_method = None
    previous_body = None

    while True:
        print("------------------------------")
        print("Pilihan Sebelumnya:")
        print(f"URL: {previous_url}")
        print(f"Metode: {previous_method}")
        print(f"Body: {previous_body}")
        print("------------------------------")

        use_previous = input("Gunakan endpoint dan metode sebelumnya? (ya/tidak): ").lower()

        if use_previous == 'ya' and previous_url:
            url, method, headers, body = get_user_input(previous_body)
        else:
            url, method, headers, body = get_user_input()

        if body is None:
            return

        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            print("URL tidak valid atau tidak menggunakan protokol HTTP atau HTTPS.")
            continue

        print("------------------------------")

        start_time = time.time()

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=json.loads(headers) if headers else {}, timeout=3600)
            elif method == "POST":
                response = requests.post(url, headers=json.loads(headers) if headers else {}, json=body, timeout=3600)

            end_time = time.time()
            total_time = end_time - start_time

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

        previous_url = url
        previous_body = body
        previous_method = method

        ulangi = input("Apakah Anda ingin menjalankan program lagi? (ya/tidak): ").lower()
        if ulangi != 'ya':
            break

if __name__ == "__main__":
    main()
