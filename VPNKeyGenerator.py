import os
import subprocess


def generate_client_keys(client_name, easy_rsa_path="/etc/openvpn/easy-rsa"):
    """
    Создает ключи и сертификаты для клиента OpenVPN.
    :param client_name: Имя клиента
    :param easy_rsa_path: Путь к директории easy-rsa
    """
    if not os.path.exists(easy_rsa_path):
        raise FileNotFoundError(f"Директория {easy_rsa_path} не найдена. Проверьте путь к easy-rsa.")

    vars_path = os.path.join(easy_rsa_path, "vars")
    if not os.path.exists(vars_path):
        raise FileNotFoundError(f"Файл {vars_path} не найден. Проверьте конфигурацию easy-rsa.")

    cmd = f"cd {easy_rsa_path} && ./easyrsa build-client-full {client_name} nopass"
    process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        print(f"Ошибка выполнения команды: {cmd}\n{process.stderr}")
        return False

    print(f"Ключи и сертификаты для клиента {client_name} созданы успешно!")
    return True
