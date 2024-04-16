import socket
import os

# Endereço e porta que o servidor vai escutar
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

# Pasta onde os arquivos estão localizados
FILES_PATH = "arquivos/"

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print("Servidor UDP esperando por requisições...")


def send_file(filename, client_address):
    try:
        with open(filename, "rb") as file:
            while True:
                data = file.read(BUFFER_SIZE)
                if not data:
                    break
                sock.sendto(data, client_address)
    except FileNotFoundError:
        print(f"Arquivo '{filename}' não encontrado.")
        sock.sendto(b"Arquivo nao encontrado", client_address)


while True:
    data, client_address = sock.recvfrom(BUFFER_SIZE)
    request = data.decode("utf-8")

    # Exemplo de protocolo simples: GET /nome_do_arquivo
    if request.startswith("GET"):
        filename = request.split()[1]
        file_path = os.path.join(FILES_PATH, filename)

        # Enviar o arquivo para o cliente
        send_file(file_path, client_address)
