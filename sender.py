import socket
import tqdm
import os
import time

# Konfigurasi server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Pilih file untuk dikirim
filename = input("Masukkan path file yang ingin dikirim: ").strip('"')
filesize = os.path.getsize(filename)

# Buat socket
client_socket = socket.socket()
print(f"[*] Menghubungkan ke {SERVER_HOST}:{SERVER_PORT}...")
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("[+] Terhubung.\n")

# Kirim informasi file (nama + ukuran)
client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

start_time = time.time()
sent_size = 0

progress = tqdm.tqdm(
    total=filesize, 
    desc=f"Mengirim {os.path.basename(filename)}", 
    unit="B", 
    unit_scale=True, 
    unit_divisor=1024,
    leave=True
)

with open(filename, "rb") as f:
    while sent_size < filesize:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        client_socket.sendall(bytes_read)
        sent_size += len(bytes_read)
        progress.update(len(bytes_read))

progress.close()
end_time = time.time()
client_socket.close()

print(f"\n[+] File berhasil dikirim dalam {end_time - start_time:.2f} detik!")
