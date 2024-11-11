pragma solidity ^0.8.0;

contract DocumentValidation {
    struct Document {
        string name;
        string hash;
    }

    // Mapeia o hash do documento para o nome
    mapping(string => Document) public documents;

    // Array para armazenar todos os documentos registrados
    Document[] public documentList;

    // Evento para documentar quando um novo documento e registrado
    event DocumentRegistered(string hash, string name);

    // Função para registrar um documento
    function registerDocument(string memory _hash, string memory _name) public {
        require(bytes(_name).length > 0, "Nome do documento e obrigatorio");
        require(bytes(_hash).length > 0, "Hash do documento e obrigatorio");

        Document memory newDocument = Document(_name, _hash);
        documents[_hash] = newDocument;
        documentList.push(newDocument);

        emit DocumentRegistered(_hash, _name);
    }

    // Função para verificar um documento registrado
    function verifyDocument(string memory _hash) public view returns (bool) {
        Document memory doc = documents[_hash];
        return bytes(doc.name).length > 0;
    }

    // Função para retornar todos os documentos registrados
    function getDocuments() public view returns (Document[] memory) {
        return documentList;
    }
}
