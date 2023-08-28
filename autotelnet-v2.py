import re
import subprocess
import time
import os
import select
import requests
from urllib.parse import urlparse
from socket import gethostbyname

def get_ip_port_from_url(url):
    # Mencari IP dan port dalam URL menggunakan regular expression
    pattern = r'https?:\/\/([^:\/]+)(?::(\d+))?(?:\/|$)'
    match = re.search(pattern, url)
    if match:
        ip = match.group(1)
        port = match.group(2) or '80'  # Menggunakan port 80 sebagai port default
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
    # Meminta masukan URL dari pengguna
    url = input("Masukkan URL: ")

    # Memeriksa protokol yang digunakan (HTTP atau HTTPS)
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        print("URL tidak valid atau tidak menggunakan protokol HTTP atau HTTPS.")
        return

    # Memisahkan IP dan port dari URL
    ip, port = get_ip_port_from_url(url)

    print("------------------------------")

    # Mengecek apakah IP dan port telah didapatkan
    if ip and port:
        # Menghasilkan teks perintah telnet
        telnet_command = f'telnet {ip} {port}'
        print("Perintah Telnet:")
        print(telnet_command)

        # Menjalankan perintah Telnet di CLI Ubuntu
        telnet_process = subprocess.Popen(telnet_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Menunggu output dari perintah Telnet, dengan batasan waktu 10 detik
        timeout = 10
        poll_obj = select.poll()
        poll_obj.register(telnet_process.stdout, select.POLLIN)
        poll_obj.register(telnet_process.stderr, select.POLLIN)

        start_time = time.time()
        output = None  # Default value untuk output
        while time.time() - start_time < timeout:
            if poll_obj.poll(0):
                output = os.read(telnet_process.stdout.fileno(), 1024).decode()
                if output:
                    print(output.strip())
            time.sleep(1)

        # Menghentikan perintah Telnet jika masih berjalan
        telnet_process.terminate()
        telnet_process.wait()

        # Memeriksa apakah ada output dalam interval waktu 10 detik
        if output:
            print("Telnet berhasil terhubung.")
            resolved_ip = get_ip_from_domain(parsed_url.hostname)
            if resolved_ip:
                ip = resolved_ip
            else:
                print(f"Tidak dapat mengambil IP dari domain {parsed_url.hostname}")
        else:
            print("Telnet tidak terhubung.")
            ip = None  # Set IP to None since Telnet failed
        
        print("------------------------------")

        # Menggunakan modul requests untuk mengirim permintaan HTTP ke endpoint
        response = None
        timeout = 3
        print('Method: GET')
        try:
            response = requests.get(url, timeout=timeout)
            print("Response dari endpoint:")
            print(f"HTTP Status Code: {response.status_code}")
            print(response.text)
        except requests.Timeout:
            print("Tidak mendapatkan respons dari endpoint (Timeout / Blacklisted IP)")

        print("------------------------------")

        # Menampilkan informasi detail endpoint
        print("Detail endpoint:")
        print(f"URL: {url}")
        print(f"IP: {ip}")
        print(f"Port: {port}")

    else:
        print("URL tidak valid atau tidak mengandung IP dan port.")

if __name__ == "__main__":
    main()
