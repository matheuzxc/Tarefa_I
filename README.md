# Projeto MQTT com Criptografia Simétrica (Fernet)

**Alunos**: Matheus Nunes Franco e Enzo Perez

Este projeto utiliza o protocolo **MQTT** (Message Queuing Telemetry Transport) para comunicação entre dois dispositivos, com a adição de **criptografia simétrica** usando a biblioteca **Fernet** para garantir a segurança das mensagens trocadas.

## Tabela de Conteúdos

- [Descrição do Projeto](#descrição-do-projeto)
- [Instalação](#instalação)
- [Como Utilizar](#como-utilizar)

## Descrição do Projeto

Este sistema consiste em dois scripts principais:

1. **Cliente**: Este script é responsável por enviar comandos ao servidor via MQTT e processar as respostas recebidas. Todas as mensagens enviadas e recebidas são criptografadas utilizando uma chave simétrica **Fernet**, garantindo que a comunicação seja segura.
  
2. **Servidor**: O servidor recebe os comandos enviados pelo cliente via MQTT, processa as informações solicitadas (como a lista de processos e usuários ativos no sistema) e envia as respostas de volta ao cliente, tudo criptografado com a chave **Fernet**.

Este sistema permite a troca de informações sensíveis entre os dispositivos de forma segura, utilizando a criptografia para proteger a privacidade dos dados.

## Instalação

### Requisitos

- **Python 3.6** ou superior
- **Mosquitto MQTT Broker**
- Bibliotecas Python:
  - `paho-mqtt` para comunicação MQTT
  - `cryptography` para criptografia com Fernet
  - `psutil` para gerenciar processos do sistema

### Passos para Instalar

1. **Instalar dependências do Python:**

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install paho-mqtt cryptography psutil
```
2. **Instalar Mosquitto MQTT Broker:**

No Ubuntu/Debian:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

No Windows:

Baixe o instalador do Mosquitto em mosquitto.org.

3. **Gerar a chave Fernet:**

```bash
from cryptography.fernet import Fernet
chave = Fernet.generate_key()
with open("chave.txt", "wb") as chave_arquivo:
    chave_arquivo.write(chave)
```

Isso criará um arquivo chave.txt com a chave gerada. Esse arquivo deve ser compartilhado entre o cliente e o servidor.

## Como utilizar

1. **Rodar o Mosquitto Broker:**
No servidor, inicie o Mosquitto:

```bash
sudo systemctl start mosquitto
```

2. **Rodar o Servidor MQTT (script do servidor):**

No servidor, execute o script responsável por gerenciar as requisições e enviar as respostas criptografadas:

```bash
python servidor.py
```


3. **Rodar o Cliente MQTT (script do cliente):**

No cliente, execute o script que envia comandos e recebe respostas do servidor:

```bash
python cliente.py
```

Quando o cliente for executado, ele exibirá essas opções no terminal, aguardando que o usuário escolha uma delas digitando o número correspondente. Dependendo da escolha:

**Opção 1: O cliente enviará o comando "obter_processos" para o servidor via MQTT.**

**Opção 2: O cliente enviará o comando "obter_usuarios" para o servidor via MQTT.**
    
**Opção 3: O cliente sairá do loop e finalizará o programa.**