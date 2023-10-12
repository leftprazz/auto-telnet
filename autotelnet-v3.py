import requests
import json
from urllib.parse import urlparse
from socket import gethostbyname
from requests.exceptions import ConnectionError

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

# ... (bagian lain dari kode Anda tetap sama)

def main():
    url, method, headers, body = get_user_input()

    if body is None:
        return

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        print("URL tidak valid atau tidak menggunakan protokol HTTP atau HTTPS.")
        return

    ip, port = get_ip_port_from_url(url)

    print("------------------------------")

    try:
        response = None
        if method == "GET":
            response = requests.get(url, headers=json.loads(headers) if headers else {}, timeout=10)
        elif method == "POST":
            # Menggunakan json.dumps untuk mengonversi dictionary body ke JSON string yang valid
            response = requests.post(url, headers=json.loads(headers) if headers else {}, data=json.dumps(body), timeout=10)

        print("Response dari endpoint:")
        print(f"HTTP Status Code: {response.status_code}")
        print(response.text)

        resolved_ip = get_ip_from_domain(parsed_url.hostname)
        if resolved_ip:
            ip = resolved_ip
        else:
            print(f"Tidak dapat mengambil IP dari domain {parsed_url.hostname}")

    except ConnectionError as e:
        print(f"Tidak mendapatkan respon dari endpoint (Error: {e})")
    except requests.Timeout:
        print("Tidak mendapatkan respons dari endpoint (Timeout)")

    print("------------------------------")

    print("Detail endpoint:")
    print(f"URL: {url}")
    print(f"IP: {ip}")
    print(f"Port: {port}")

if __name__ == "__main__":
    main()
