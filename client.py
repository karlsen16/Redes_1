import socket
import os

# Endereço e porta do servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Pasta onde os arquivos serão salvos
SAVE_FOLDER = "arquivos_recebidos"

def receive_file(arquivo, client_socket):
    save_path = os.path.join(SAVE_FOLDER, filename)
    with open(save_path, "wb") as file:
        while True:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            if data == b"Arquivo nao encontrado":
                print(f"Arquivo '{arquivo}' não encontrado no servidor.")
                break
            file.write(data)
            if len(data) < BUFFER_SIZE:
                break
        print(f"Arquivo '{arquivo}' recebido e salvo em '{save_path}'.")


# Criação do socket UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Solicitar arquivo ao usuário
    filename = input("Digite o nome do arquivo (ou sair): ")

    if filename.lower() == "sair":
        break

    # Enviar a requisição ao servidor
    request = f"GET {filename}"
    client_sock.sendto(request.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

    # Receber o arquivo do servidor
    receive_file(filename, client_sock)

print("Cliente encerrado.")
# Fechar o socket do cliente
client_sock.close()
