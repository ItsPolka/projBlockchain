import threading
from urllib.parse import urlparse

import requests

from block import Block

MAX_NONCE = 2 ** 200


class Blockchain:
    def __init__(self, difficulty: int):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.difficulty = difficulty
        self.lock = threading.Lock()

    def new_block(self, transaction):
        """
        Mina un bloque nuevo. Puede ser llamado por varios hilos al mismo
        tiempo (varias personas conectadas intentando minar); el lock al
        final decide quién gana si dos hilos terminan casi simultáneo.
        """
        previous_hash = self.last_block.hash if self.chain else "0"
        index = len(self.chain)
        nblock = Block(index, transaction, previous_hash)
        success = nblock.mine_block(self.difficulty, self)

        if not success:
            return None

        with self.lock:
            # Revalidar dentro del lock: alguien pudo haber ganado
            # la carrera justo antes de llegar aquí.
            if len(self.chain) == nblock.index:
                self.chain.append(nblock)
                return nblock

        return None

    def add_node(self, address: str):
        """
        Registra un nuevo nodo, ej: 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # aceptar direcciones sin esquema, ej '192.168.0.5:5000'
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError(f"URL de nodo inválida: {address}")

    def valid_chain(self, chain) -> bool:
        """
        Verifica que una cadena recibida de otro nodo sea válida:
        que el previous_hash encadene correctamente y que cada bloque
        cumpla la dificultad requerida.
        """
        if not chain:
            return False

        for i in range(len(chain)):
            block_data = chain[i]

            rebuilt = Block(
                block_data["index"],
                block_data["transaction"],
                block_data["previous_hash"],
            )
            rebuilt.timestamp = block_data["timestamp"]
            rebuilt.nonce = block_data["nonce"]
            recalculated_hash = rebuilt.calculate_hash()

            if recalculated_hash != block_data["hash"]:
                return False

            if block_data["hash"][: self.difficulty] != "0" * self.difficulty:
                return False

            if i > 0:
                previous_block = chain[i - 1]
                if block_data["previous_hash"] != previous_block["hash"]:
                    return False

        return True

    def resolve_conflicts(self) -> bool:
        """
        Algoritmo de consenso: reemplaza nuestra cadena por la más larga
        válida entre todos los nodos registrados.
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f"http://{node}/chain", timeout=5)
            except requests.exceptions.RequestException:
                continue

            if response.status_code == 200:
                data = response.json()
                length = data["length"]
                chain = data["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            with self.lock:
                self.chain = [
                    Block(b["index"], b["transaction"], b["previous_hash"])
                    for b in new_chain
                ]
                for block, data in zip(self.chain, new_chain):
                    block.timestamp = data["timestamp"]
                    block.nonce = data["nonce"]
                    block.hash = data["hash"]
            return True

        return False

    @property
    def last_block(self) -> Block:
        """
        Regresa el último Block de la cadena
        """
        return self.chain[-1]
