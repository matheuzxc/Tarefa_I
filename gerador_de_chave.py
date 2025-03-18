from cryptography.fernet import Fernet

chave = Fernet.generate_key()
print(f"Sua chave secreta: {chave.decode()}")
