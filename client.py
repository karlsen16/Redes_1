import socket
import os
import shutil

# Endereço e porta do servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Pasta onde os arquivos serão salvos
SAVE_FOLDER = "arquivos_recebidos"


def receive_file(arquivo, client_socket):
    save_path_r = os.path.join(SAVE_FOLDER, arquivo)
    with open(save_path_r, "wb") as file:
        while True:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            if data == b"Arquivo nao encontrado":
                print(f"Arquivo '{arquivo}' não encontrado no servidor.")
                break
            file.write(data)
            if len(data) < BUFFER_SIZE:
                break
        print(f"Arquivo '{arquivo}' recebido e salvo em '{save_path_r}'.")
        return save_path_r


def calculate_checksum(arquivo_check):
    # Simulação simples de checksum: soma dos bytes do arquivo
    with open(arquivo_check, "rb") as file:
        checksum = sum(bytearray(file.read()))
    return checksum


def discard_data(save_path_):
    # Simula descartar uma parte do arquivo (deleta metade)
    try:
        file_size = os.path.getsize(save_path_)
        with open(save_path_, "rb+") as file:
            file.truncate(file_size // 2)
        print("Parte do arquivo foi descartada.")
    except Exception as e:
        print(f"Erro ao descartar parte do arquivo: {e}")


def verify_file(arquivo_verify, expected_checksum_):
    calculated_checksum = calculate_checksum(arquivo_verify)
    return calculated_checksum == expected_checksum_


# Criação do socket UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Verifica se a pasta de arquivos recebidos existe, se não, cria
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

novo_get = True
filename = ""
counter = 0
tent_max = 2
while True:
    if novo_get:
        # Solicitar arquivo ao usuário
        filename = input("\n############\nDigite o nome do arquivo (ou sair): ")
        if filename.lower() == "sair":
            break

        # Enviar a requisição ao servidor
        request = f"GET {filename}"
        client_sock.sendto(request.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

    # Receber o arquivo do servidor
    save_path = receive_file(filename, client_sock)

    # Calcular checksum do arquivo recebido
    expected_checksum = int(client_sock.recvfrom(BUFFER_SIZE)[0].decode('utf-8'))
    is_valid = verify_file(save_path, expected_checksum)

    if is_valid:
        print("\n############\nArquivo recebido e checksum conferem. Deseja descartar uma parte do arquivo?")
        discard_option = input("Digite 'sim' para descartar uma parte, ou qualquer outra coisa para manter: ")

        if discard_option.lower() == "sim":
            discard_data(save_path)

        print(f"Arquivo '{filename}' está pronto para uso.\n############\n")
        novo_get = True
        counter = 0
    else:
        if counter < tent_max:
            print("Erro: O arquivo recebido está corrompido.")
            print("Solicitando ao servidor para reenviar as partes faltando...")
            print("(Tentativas restantes:", tent_max-counter, ")")
            resend_request = f"RESEND {filename} {os.path.getsize(save_path)}"
            client_sock.sendto(resend_request.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
            novo_get = False
            counter += 1
        else:
            print("Máximo de tentativas excedido.\n########################\n")
            novo_get = True
            counter = 0

# Remove a pasta de arquivos recebidos
shutil.rmtree("arquivos_recebidos")

print("Cliente encerrado.")
# Fechar o socket do cliente
client_sock.close()
