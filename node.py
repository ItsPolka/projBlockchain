from argparse import ArgumentParser
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)

# Identificador único de este nodo/instancia
node_identifier = str(uuid4()).replace("-", "")

# Ajusta la dificultad según qué tan rápido quieres que se minen bloques
blockchain = Blockchain(difficulty=4)


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json(silent=True)
    if not values or "transaction" not in values:
        return jsonify({"message": "Falta el campo 'transaction'"}), 400

    blockchain.current_transactions.append(values["transaction"])
    return jsonify({"message": "Transacción agregada al pool"}), 201


@app.route("/mine", methods=["POST"])
def mine():
    """
    Cada persona conectada le pega a este endpoint para intentar minar
    el siguiente bloque. Flask corre con threaded=True, así que varias
    peticiones simultáneas compiten de verdad por el mismo bloque.
    """
    values = request.get_json(silent=True) or {}
    transaction = values.get("transaction")

    if not transaction:
        if blockchain.current_transactions:
            transaction = blockchain.current_transactions.pop(0)
        else:
            return jsonify({"message": "No hay transacciones pendientes para minar"}), 200

    block = blockchain.new_block(transaction)

    if block is None:
        return jsonify({
            "message": "Llegaste tarde: alguien más ya minó este bloque",
        }), 409

    response = {
        "message": "¡Nuevo bloque minado!",
        "index": block.index,
        "hash": block.hash,
        "nonce": block.nonce,
        "miner": node_identifier,
    }
    return jsonify(response), 200


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": [block.to_dict() for block in blockchain.chain],
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json(silent=True)
    nodes = values.get("nodes") if values else None

    if nodes is None:
        return jsonify({"message": "Error: manda una lista de nodos"}), 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        "message": "Nodos agregados",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            "message": "Nuestra cadena fue reemplazada",
            "new_chain": [block.to_dict() for block in blockchain.chain],
        }
    else:
        response = {
            "message": "Nuestra cadena sigue siendo la válida",
            "chain": [block.to_dict() for block in blockchain.chain],
        }

    return jsonify(response), 200


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="puerto en el que corre este nodo"
    )
    args = parser.parse_args()

    # threaded=True es necesario para que varias personas puedan intentar
    # minar al mismo tiempo contra este mismo proceso/blockchain.
    app.run(host="0.0.0.0", port=args.port, threaded=True)
