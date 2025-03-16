import paho.mqtt.client as mqtt


def connectMqtt(client, userdata, flags, rc):
    print(f"Conectado com sucesso, código de resultado: {rc}")


def gerenciamentoRequisições(client, userdata, msg):
    
    print(f"Tópico: {msg.topic}")
    print(f"Mensagem: {msg.payload.decode()}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = connectMqtt
mqtt_client.on_message = gerenciamentoRequisições
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.subscribe("sistema/processos")
mqtt_client.subscribe("sistema/usuarios")


mqtt_client.loop_start()

def enviaComando(comando):
    mqtt_client.publish("sistema/comandos", comando)

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
