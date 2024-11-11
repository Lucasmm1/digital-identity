import time

class Identity:
    def __init__(self, name, unique_id):
        self.name = name
        self.unique_id = unique_id
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'name': self.name,
            'unique_id': self.unique_id,
            'timestamp': self.timestamp
        }

def register_identity(blockchain, name, unique_id, document_hash=None):
    identity = Identity(name, unique_id)
    identity_dict = identity.to_dict()
    identity_dict['document_hash'] = document_hash  # Garante que 'document_hash' exista
    blockchain.add_identity(identity_dict)
    print(f"Identidade de {name} registrada com sucesso.")