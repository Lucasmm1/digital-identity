def verify_identity(blockchain, document_hash):
    for identity in blockchain.identities:
        if 'document_hash' in identity and identity['document_hash'] == document_hash:
            return True, identity
    return False, None

def check_identity(blockchain, unique_id):
    exists, identity = verify_identity(blockchain, unique_id)
    if exists:
        print(f"Identidade verificada: {identity['name']}, ID: {identity['unique_id']}")
    else:
        print("Identidade não encontrada.")
