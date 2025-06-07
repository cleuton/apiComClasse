from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados de exemplo
itens = [
    {"id": 1, "nome": "Item 1", "preco": 10.0},
    {"id": 2, "nome": "Item 2", "preco": 20.0},
]

# Rota para obter todos os itens
@app.route('/obter/itens', methods=['GET'])
def obter_itens():
    return jsonify(itens)

# Rota para filtrar itens por nome
# curl -X post -H "Content-type: application/json" -d'{"filtro": "\"1\" in x[\"nome\"]"}' http://localhost:8080/filtrar-itens
@app.route('/filtrar-itens', methods=['POST'])
def filtrar_itens():
    # RECEBE UM ATRIBUTO DO CLIENTE COMO STRING
    filtro_item = request.json.get('filtro')
    try:
        # CRIA UMA FUNÇÃO A PARTIR DA STRING RECEBIDA
        filtro_func = eval(f"lambda x: {filtro_item}")
        
        # FILTRA OS USUÁRIOS COM BASE NO FILTRO DO CLIENTE
        resultado = list(filter(filtro_func, itens))
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

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
    return jsonify("Item criado"), 200

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

