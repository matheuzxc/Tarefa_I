import paho.mqtt.client as mqtt
import psutil
import os
import time
from cryptography.fernet import Fernet

def carregar_chave():
    with open("chave_b.txt", "rb") as f:
        return f.read()

CHAVE = carregar_chave()
cipher = Fernet(CHAVE)

def connectMqtt(client, userdata, flags, rc):
    print(f"Conectado com o código de retorno {rc}")
    client.subscribe("sistema/comandos")

def gerenciamentoRequisições(client, userdata, msg):
    try:
        comando = cipher.decrypt(msg.payload).decode()
        print(f"Comando recebido: {comando}")

        if comando == "obter_processos":
            publicarProcessos(client)
        elif comando == "obter_usuarios":
            publicarUsuarios(client)
        else:
            print(f"Comando não reconhecido: {comando}")
    except Exception as e:
        print(f"Erro na descriptografia: {str(e)}")

def publicarProcessos(client):
    processos = []

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            processos.append(f"PID: {proc.info['pid']} - Nome: {proc.info['name']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        processos.append("Erro ao acessar lista de processos")

    mensagem_criptografada = cipher.encrypt("\n".join(processos).encode())
    client.publish("sistema/processos", mensagem_criptografada)

def publicarUsuarios(client):
    usuarios = []

    try:
        pc_user = os.popen('who').readlines()
        for user in pc_user:
            usuarios.append(user.strip())
    except Exception as e:
        usuarios.append(f"Erro ao obter usuários: {str(e)}")

    mensagem_criptografada = cipher.encrypt("\n".join(usuarios).encode())
    client.publish("sistema/usuarios", mensagem_criptografada)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = connectMqtt
mqtt_client.on_message = gerenciamentoRequisições
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Finalizando o serviço MQTT...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
