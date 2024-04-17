import socket
import os

# Endereço e porta que o servidor vai escutar
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

# Pasta onde os arquivos estão localizados
FILES_PATH = "arquivos/"


def send_file_chunk(arquivo_chunk, client_address_chunk, client_sock, start_byte_chunk):
    file_path = os.path.join(FILES_PATH, arquivo_chunk)
    try:
        with open(file_path, "rb") as file:
            file.seek(start_byte_chunk)
            dados_chunk = file.read(BUFFER_SIZE)
            if not dados_chunk:
                client_sock.sendto(b"", client_address_chunk)  # Envie um pedaço vazio para indicar o final do arquivo
            else:
                client_sock.sendto(dados_chunk, client_address_chunk)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo_chunk}' não encontrado.")
        client_sock.sendto(b"Arquivo nao encontrado", client_address_chunk)


# def send_file(arquivo_s, end_cliente, client_sock):
#     file_path_s = os.path.join(FILES_PATH, arquivo_s)
#     try:
#         with open(file_path_s, "rb") as file:
#             while True:
#                 dados_s = file.read(BUFFER_SIZE)
#                 if not dados_s:
#                     break
#                 client_sock.sendto(dados_s, end_cliente)
#             # Enviar checksum do arquivo
#             checksum = calculate_checksum(file_path_s)
#             client_sock.sendto(str(checksum).encode('utf-8'), end_cliente)
#     except FileNotFoundError:
#         print(f"Arquivo '{arquivo_s}' não encontrado.")
#         client_sock.sendto(b"Arquivo nao encontrado", end_cliente)


def calculate_checksum(arquivo_c):
    # Simulação simples de checksum: soma dos bytes do arquivo
    with open(arquivo_c, "rb") as file:
        checksum = sum(bytearray(file.read()))
    return checksum


# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print("Servidor UDP esperando por requisições...")

while True:
    data, client_address = sock.recvfrom(BUFFER_SIZE)
    request = data.decode("utf-8")

    # Exemplo de protocolo simples: GET /nome_do_arquivo
    if request.startswith("GET"):
        filename = request.split()[1]
        # Enviar o arquivo para o cliente
        send_file_chunk(filename, client_address, sock, 0)
        print("GET ativado")

    # Receber requisição de reenvio de partes
    elif request.startswith("RESEND"):
        filename = request.split()[1]
        # Enviar o arquivo novamente para o cliente
        start_byte = int(request.split()[2])
        # Enviar o arquivo a partir do byte especificado
        send_file_chunk(filename, client_address, sock, start_byte)
        print("RESEND ativado")
