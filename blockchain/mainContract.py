from web3 import Web3
import json
import time
from blockchain import Blockchain
from identidade import register_identity
from utils import check_identity, verify_identity

# Configuração da rede Ethereum com Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))  # servidor local (ganache)
contract_address = '0x55678600d64Dab7DF819848E8a923cFc430bb0D8'  # Endereço do contrato
from_account = '0xeCad4E3d028184de552B195343B6b88Fa70B1978'  # Endereço da conta etherium
private_key = '0x954f5c0b3528bbc5c691845456c7281dd460f596ea3fe7bbb24581f2ae333205'  #chave privada

# ABI do contrato (carregada previamente do arquivo JSON)
contract_abi = [
    {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'hash', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'name', 'type': 'string'}], 'name': 'DocumentRegistered', 'type': 'event'},
    {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'documentList', 'outputs': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'string', 'name': 'hash', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'},
    {'inputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'name': 'documents', 'outputs': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'string', 'name': 'hash', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'},
    {'inputs': [{'internalType': 'string', 'name': '_hash', 'type': 'string'}, {'internalType': 'string', 'name': '_name', 'type': 'string'}], 'name': 'registerDocument', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
    {'inputs': [{'internalType': 'string', 'name': '_hash', 'type': 'string'}], 'name': 'verifyDocument', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'},
    {'inputs': [], 'name': 'getDocuments', 'outputs': [{'components': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'string', 'name': 'hash', 'type': 'string'}], 'internalType': 'struct DocumentValidation.Document[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}
]

# Criar o objeto do contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Inicializar a blockchain local
my_blockchain = Blockchain()

# Função para registrar identidade localmente e no contrato Ethereum
def register_document_locally_and_on_contract(name, unique_id, document_hash, document_name):
    # Registrar a identidade na blockchain local
    register_identity(my_blockchain, name, unique_id)

    # Registrar o documento na blockchain local (no blockchain.py)
    my_blockchain.add_identity({
        'name': name,
        'unique_id': unique_id,
        'document_hash': document_hash,
        'document_name': document_name,
        'timestamp': time.time()
    })

    # Minerar o bloco após adicionar a identidade e o documento
    my_blockchain.mine_block()

    # Registrar o documento no contrato inteligente da Ethereum
    transaction = contract.functions.registerDocument(document_hash, document_name).build_transaction({
        'chainId': 1337,
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': w3.eth.get_transaction_count(from_account),
    })

    # Assinar e enviar a transação
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Documento registrado no contrato. Transação hash: {txn_hash.hex()}")

    print("Identidades armazenadas localmente:", my_blockchain.identities)

# Função para verificar documentos na blockchain local e no contrato inteligente
def verify_document_locally_and_on_contract(document_hash):
    # Verificar localmente (na blockchain Python)
    exists, identity = verify_identity(my_blockchain, document_hash)
    if exists:
        print(f"Documento encontrado na blockchain local: {identity}")
    else:
        print("Documento não encontrado na blockchain local.")
    
    # Verificar no contrato inteligente Ethereum
    is_verified = contract.functions.verifyDocument(document_hash).call()
    print(f"Documento verificado na blockchain Ethereum: {is_verified}")

# Exemplo de uso
document_hash = '4e4f2c5f6a1e2b2dbf8b3d37d1a1576a57e4f7e1ab0a3f0a10f7fe8a7d7bcf8c'
document_name = 'Documento Exemplo'
name = 'Alice'
unique_id = 'ID12345'

# Registrar o documento localmente e no contrato Ethereum
register_document_locally_and_on_contract(name, unique_id, document_hash, document_name)

# Verificar o documento localmente e no contrato Ethereum
verify_document_locally_and_on_contract(document_hash)

# Exibir as identidades armazenadas localmente
print("Identidades armazenadas localmente:", my_blockchain.identities)
