import hashlib
import json
from time import time


class Block:
    def __init__(self, index, transaction, previous_hash):
        self.index = index
        self.timestamp = time()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transaction": self.transaction,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        return (
            f"Block(index={self.index}, hash={self.hash[:10]}..., "
            f"previous_hash={self.previous_hash[:10] if self.previous_hash else 'None'}..., "
            f"nonce={self.nonce})"
        )