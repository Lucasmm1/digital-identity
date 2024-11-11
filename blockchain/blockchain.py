import hashlib
import time

class Blockchain:
    def __init__(self):
        # Inicializa a blockchain com um bloco génesis
        self.chain = []
        self.create_block(previous_hash='0')
        self.identities = []  # Lista para armazenar as identidades globalmente (fora da blockchain)

    def add_identity(self, identity):
        """
        Adiciona uma identidade tanto ao último bloco da cadeia quanto à lista global de identidades.
        """
        last_block = self.get_last_block()
        last_block['identities'].append(identity)  # Adiciona a identidade ao bloco atual
        self.identities.append(identity)  # Adiciona a identidade à lista global de identidades

    def create_block(self, previous_hash):
        """
        Cria um novo bloco e o adiciona à cadeia.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'previous_hash': previous_hash,
            'identities': []  # Cada bloco tem uma lista de identidades
        }
        self.chain.append(block)
        return block

    def get_last_block(self):
        """
        Retorna o último bloco da cadeia.
        """
        return self.chain[-1]

    def hash(self, block):
        """
        Gera o hash de um bloco.
        """
        encoded_block = str(block).encode()  # Codifica o bloco como uma string
        return hashlib.sha256(encoded_block).hexdigest()  # Retorna o hash SHA-256

    def mine_block(self):
        """
        Cria um novo bloco, adiciona à cadeia e retorna o novo bloco.
        """
        last_block = self.get_last_block()
        previous_hash = self.hash(last_block)  # Calcula o hash do último bloco
        new_block = self.create_block(previous_hash)  # Cria o novo bloco
        return new_block
