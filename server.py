import socket
import tqdm
import os
import signal
import sys

# Konfigurasi server
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
DATA_FOLDER = "data"

# Buat folder data
os.makedirs(DATA_FOLDER, exist_ok=True)

# Buat socket server
server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
server_socket.settimeout(1)

print(f"[*] Menunggu koneksi di {SERVER_HOST}:{SERVER_PORT}...")

# Flag untuk kontrol shutdown
shutdown_flag = False  

def signal_handler(sig, frame):
    global shutdown_flag
    print("\n[!] Menutup server...")
    shutdown_flag = True
    server_socket.close()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while not shutdown_flag:
    try:
        # Menerima koneksi baru
        client_socket, address = server_socket.accept()
        print(f"[+] Terhubung ke {address}\n")
        
        # Menerima informasi file
        received = client_socket.recv(BUFFER_SIZE).decode()
        if not received:
            client_socket.close()
            continue
            
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        filepath = os.path.join(DATA_FOLDER, filename)

        # Proses menerima file
        progress = tqdm.tqdm(
            total=filesize,
            desc=f"Menerima {filename}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024
        )

        with open(filepath, "wb") as f:
            while True:
                if shutdown_flag:
                    print("\n[!] Server dimatikan paksa, aborting transfer...")
                    raise KeyboardInterrupt
                    
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        progress.close()
        print(f"\n[+] File '{filename}' berhasil disimpan di '{DATA_FOLDER}'!\n")
        client_socket.close()

    except socket.timeout:
        continue 
    except KeyboardInterrupt:
        break     # Keluar loop jika ada interrupt
    except Exception as e:
        if not shutdown_flag:
            print(f"[ERROR] Terjadi kesalahan: {str(e)}")

server_socket.close()
print("[!] Server telah dimatikan.")
sys.exit(0)