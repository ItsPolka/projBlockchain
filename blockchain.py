import hashlib
import json
from time import time

"""
Code provided by:   @katakakikita
https://medium.com/@katakakikita/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03
"""

MAX_NONCE = 2 ** 200

class Blockchain:
    def __init__(self):
        self.index=index
        self.timestamp=timestamp
        self.transaction=transaction
        self.previous_hash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100, sender="", recipient="", amount="")

    def new_block(self, index,timestamp,transaction,previousHash,nonce):

# Hola mundo
        pass


    @staticmethod
    def calculate_hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """
        pass

    @property
    def last_block(self):
        """
        Returns the last Block in the chain
        """
        pass

    @staticmethod
    def mine_block(transaction, last_hash, target):
        header = {
            'last_hash': last_hash,
            'transaction_hash': Blockchain.calculate_hash(transaction),
            'time': time,
            'target': target,
            'nonce': 0
        }
        while True:
            result_hash = hashlib.sha256(hashlib.sha256(json.dumps(header).encode()).digest())
            if result_hash < target:
                return (header, result_hash)
            header['nonce'] += 1

            if header['nonce'] > MAX_NONCE:
                header['time'] = time
                header['nonce'] = 0
