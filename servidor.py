import paho.mqtt.client as mqtt
import psutil
import os
import time

# Callback de conexão ao broker MQTT
def connectMqtt(client, userdata, flags, rc):
    print(f"Conectado com o código de retorno {rc}")
    client.subscribe("sistema/comandos")

# Callback para gerenciamento de requisições recebidas pelo MQTT
def gerenciamentoRequisições(client, userdata, msg):
    comando = msg.payload.decode()
    print(f"Comando recebido: {comando}")

    if comando == "obter_processos":
        publicarProcessos(client)
    elif comando == "obter_usuarios":
        publicarUsuarios(client)
    else:
        print(f"Comando não reconhecido: {comando}")

# Publica a lista de processos ativos
def publicarProcessos(client):
    processos = []

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            processos.append(f"PID: {proc.info['pid']} - Nome: {proc.info['name']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        processos.append("Erro ao acessar lista de processos")

    # Publica os processos ou uma mensagem indicando que não há processos disponíveis
    client.publish("sistema/processos", "\n".join(processos) if processos else "Nenhum processo encontrado.")

# Publica a lista de usuários ativos
def publicarUsuarios(client):
    usuarios = []

    try:
        pc_user = os.popen('who').readlines()
        for user in pc_user:
            usuarios.append(user.strip())
    except Exception as e:
        usuarios.append(f"Erro ao obter usuários: {str(e)}")

    # Publica os usuários ou uma mensagem indicando que não há usuários ativos
    client.publish("sistema/usuarios", "\n".join(usuarios) if usuarios else "Nenhum usuário ativo encontrado.")

# Configura o cliente MQTT
mqtt_client = mqtt.Client()

# Define as funções de callback
mqtt_client.on_connect = connectMqtt
mqtt_client.on_message = gerenciamentoRequisições

# Conecta ao broker MQTT (localhost na porta 1883)
mqtt_client.connect("localhost", 1883, 60)

# Inicia o loop de rede para manter a conexão ativa
mqtt_client.loop_start()

# Mantém o programa rodando esperando comandos
if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Finalizando o serviço MQTT...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
