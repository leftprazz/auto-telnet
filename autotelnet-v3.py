import re
import subprocess
import time
import os
import select
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
    pattern = r'https?://([^:/]+)(?::(\d+))?(?:/|$)'
    match = re.search(pattern, url)
    if match:
        ip = match.group(1)
        port = match.group(2) or '80'
        return ip, port
    else:
        return None, None

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

    if ip and port:
        telnet_command = f'telnet {ip} {port}'
        print("Perintah Telnet:")
        print(telnet_command)

        telnet_process = subprocess.Popen(telnet_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        timeout = 10
        poll_obj = select.poll()
        poll_obj.register(telnet_process.stdout, select.POLLIN)
        poll_obj.register(telnet_process.stderr, select.POLLIN)

        start_time = time.time()
        output = None
        while time.time() - start_time < timeout:
            if poll_obj.poll(0):
                output = os.read(telnet_process.stdout.fileno(), 1024).decode()
                if output:
                    print(output.strip())
            time.sleep(1)

        telnet_process.terminate()
        telnet_process.wait()

        if output:
            print("Telnet berhasil terhubung.")
            resolved_ip = get_ip_from_domain(parsed_url.hostname)
            if resolved_ip:
                ip = resolved_ip
            else:
                print(f"Tidak dapat mengambil IP dari domain {parsed_url.hostname}")
        else:
            print("Telnet tidak terhubung.")
            ip = "None - Cannot get IP address"

        print("------------------------------")

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=json.loads(headers) if headers else {}, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, headers=json.loads(headers) if headers else {}, data=body, timeout=timeout)
            # tambahkan blok if untuk metode HTTP lainnya (PUT, DELETE, dll.) sesuai kebutuhan

            print("Response dari endpoint:")
            print(f"HTTP Status Code: {response.status_code}")
            print(response.text)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

        print("------------------------------")

        print("Detail endpoint:")
        print(f"URL: {url}")
        print(f"IP: {ip}")
        print(f"Port: {port}")

    else:
        print("URL tidak valid atau tidak mengandung IP dan port.")

if __name__ == "__main__":
    main()
