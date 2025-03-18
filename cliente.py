import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

def carregar_chave():
    with open("chave_a.txt", "rb") as f:
        return f.read()

CHAVE = carregar_chave()
cipher = Fernet(CHAVE)

def connectMqtt(client, userdata, flags, rc):
    print(f"Conectado com sucesso, código de resultado: {rc}")

def gerenciamentoRequisições(client, userdata, msg):
    try:
        mensagem_descriptografada = cipher.decrypt(msg.payload).decode()
        print(f"Tópico: {msg.topic}")
        print(f"Mensagem descriptografada: {mensagem_descriptografada}")
    except Exception as e:
        print(f"Erro na descriptografia: {str(e)}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = connectMqtt
mqtt_client.on_message = gerenciamentoRequisições
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.subscribe("sistema/processos")
mqtt_client.subscribe("sistema/usuarios")
mqtt_client.loop_start()

def enviaComando(comando):
    comando_criptografado = cipher.encrypt(comando.encode())
    mqtt_client.publish("sistema/comandos", comando_criptografado)

if __name__ == "__main__":
    while True:
        print("\n[1] Obter Processos")
        print("[2] Obter Usuários")
        print("[3] Sair")

        escolha = input("Escolha a opção: ")

        if escolha == "1":
            enviaComando("obter_processos")
        elif escolha == "2":
            enviaComando("obter_usuarios")
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
