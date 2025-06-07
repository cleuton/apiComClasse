from flask import Flask, jsonify, request, url_for, make_response

app = Flask(__name__)

# Dados de exemplo
itens = [
    {"id": 1, "nome": "Item 1", "preco": 10.0},
    {"id": 2, "nome": "Item 2", "preco": 20.0},
]

# Rota para obter todos os itens ou filtrar
# curl -i "http://localhost:8080/itens?nome=1"
@app.route('/itens', methods=['GET'])
def obter_itens():
    termo = request.args.get('nome')
    if termo: 
        # Filtra os itens pelo nome se o parâmetro 'nome' for fornecido
        resultado = [item for item in itens if termo.lower() in item['nome'].lower()]
        return jsonify(resultado)
    return jsonify(itens)

# Rota para obter um único item pelo ID
@app.route('/itens/<int:id_item>', methods=['GET'])
def obter_item(id_item):
    item = next((item for item in itens if item["id"] == id_item), None)
    if item:
        return jsonify(item)
    return jsonify({"erro": "Item não encontrado"}), 404

# Rota para criar um novo item
@app.route('/itens', methods=['POST'])
def criar_item():
    dados = request.get_json()
    novo_item = {
        "id": len(itens) + 1,
        "nome": dados["nome"],
        "preco": dados["preco"]
    }
    itens.append(novo_item)

    # gera URI /itens/5
    location = f"/itens/{novo_item['id']}"

    # opção 1: make_response e adiciona header manualmente
    resp = make_response(jsonify(novo_item), 201)
    resp.headers['Location'] = location
    return resp

# Rota para atualizar um item pelo ID
@app.route('/itens/<int:id_item>', methods=['PUT'])
def atualizar_item(id_item):
    dados = request.get_json()
    item = next((item for item in itens if item["id"] == id_item), None)
    if item:
        item["nome"] = dados.get("nome", item["nome"])
        item["preco"] = dados.get("preco", item["preco"])
        return jsonify(item)
    return jsonify({"erro": "Item não encontrado"}), 404

# Rota para deletar um item pelo ID
@app.route('/itens/<int:id_item>', methods=['DELETE'])
def deletar_item(id_item):
    global itens
    itens = [item for item in itens if item["id"] != id_item]
    return jsonify({"mensagem": "Item deletado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

