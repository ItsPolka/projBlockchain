import hashlib
import json
from time import time
#hola

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Create the genesis block
        self.new_block(previous_hash="1", nonce=100)

    def new_block(self, nonce, previous_hash=None):
        """
        Creates a new block and adds it to the chain.
        """
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "nonce": nonce,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # Reset pending transactions after including them in a block
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of pending transactions.
        Returns the index of the block that will hold this transaction.
        """
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block.
        """
        # Sort keys so the hash is consistent regardless of dict ordering
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns the last block in the chain.
        """
        return self.chain[-1]


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.new_transaction("Alice", "Bob", 5)
    blockchain.new_block(nonce=12345)

    print(json.dumps(blockchain.chain, indent=2))