from flask import Flask, jsonify, request, url_for, make_response

app = Flask(__name__)

# dados de exemplo
itens = [
    {"id": 1, "nome": "Item 1", "preco": 10.0},
    {"id": 2, "nome": "Item 2", "preco": 20.0},
]

def adiciona_links_item(item):
    res = item.copy()
    res["links"] = {
        "self":        url_for("obter_item",     id_item=res["id"]),
        "update":      url_for("atualizar_item", id_item=res["id"]),
        "delete":      url_for("deletar_item",   id_item=res["id"]),
        "collection":  url_for("obter_itens"),
        "create":      url_for("criar_item"),
    }
    return res

@app.route('/itens', methods=['GET'])
def obter_itens():
    termo = request.args.get('nome')
    filtrados = itens
    if termo:
        filtrados = [i for i in itens if termo.lower() in i["nome"].lower()]

    resposta = {
        "itens": [adiciona_links_item(i) for i in filtrados],
        "links": {
            "self":   url_for("obter_itens", nome=termo) if termo else url_for("obter_itens"),
            "create": url_for("criar_item"),
        }
    }
    return jsonify(resposta)

@app.route('/itens/<int:id_item>', methods=['GET'])
def obter_item(id_item):
    item = next((i for i in itens if i["id"] == id_item), None)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    return jsonify(adiciona_links_item(item))

@app.route('/itens', methods=['POST'])
def criar_item():
    dados = request.get_json()
    novo = {"id": len(itens) + 1, "nome": dados["nome"], "preco": dados["preco"]}
    itens.append(novo)

    payload = adiciona_links_item(novo)
    resp = make_response(jsonify(payload), 201)
    resp.headers["Location"] = url_for("obter_item", id_item=novo["id"])
    return resp

@app.route('/itens/<int:id_item>', methods=['PUT'])
def atualizar_item(id_item):
    dados = request.get_json()
    item = next((i for i in itens if i["id"] == id_item), None)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    item["nome"]  = dados.get("nome",  item["nome"])
    item["preco"] = dados.get("preco", item["preco"])
    return jsonify(adiciona_links_item(item))

@app.route('/itens/<int:id_item>', methods=['DELETE'])
def deletar_item(id_item):
    global itens
    alvo = next((i for i in itens if i["id"] == id_item), None)
    if not alvo:
        return jsonify({"erro": "Item não encontrado"}), 404
    itens = [i for i in itens if i["id"] != id_item]
    return jsonify({
        "mensagem": "Item deletado",
        "links": {
            "collection": url_for("obter_itens"),
            "create":     url_for("criar_item")
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
