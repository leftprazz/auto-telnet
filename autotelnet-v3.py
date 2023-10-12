import requests
import json
from urllib.parse import urlparse
from socket import gethostbyname
from requests.exceptions import ConnectionError

def get_user_input():
    url = input("Masukkan URL: ")
    method = input("Pilih Metode HTTP (GET/POST/PUT/DELETE, dll.): ").upper()
    headers = input("Masukkan Headers (opsional, contoh: 'key:value,key2:value2'): ").strip()
    body = input("Masukkan Body (opsional, untuk metode POST/PUT, dll.): ").strip()

    return url, method, headers, body

def get_ip_port_from_url(url):
    parsed_url = urlparse(url)
    ip = parsed_url.hostname
    port = parsed_url.port or 80

    return ip, port

def get_ip_from_domain(domain):
    try:
        ip = gethostbyname(domain)
        return ip
    except:
        return None

def main():
    url, method, headers, body = get_user_input()

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
            response = requests.post(url, headers=json.loads(headers) if headers else {}, data=body, timeout=10)
        # tambahkan blok if untuk metode HTTP lainnya (PUT, DELETE, dll.) sesuai kebutuhan

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
