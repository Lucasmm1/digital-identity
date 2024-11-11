from blockchain import Blockchain
from identidade import register_identity
from utils import check_identity

# Inicializa a blockchain
my_blockchain = Blockchain()

# Registro de identidades
register_identity(my_blockchain, "Alice", "ID12345")
register_identity(my_blockchain, "Bob", "ID67890")

# "Minerar" um novo bloco para adicionar as identidades
my_blockchain.mine_block()

# Verificar identidades
check_identity(my_blockchain, "ID12345")
check_identity(my_blockchain, "ID00000")
