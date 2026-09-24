import hashlib
import json
from time import time
from block import Block

"""
Code provided by:   @katakakikita
https://medium.com/@katakakikita/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03
"""

MAX_NONCE = 2 ** 200

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

    def new_block(self, transaction):
        nblock = Block(len(self.chain), transaction, Block.calculate_hash(self.last_block))
        self.chain.append(nblock)

    @property
    def last_block(self):
        """
        Returns the last Block in the chain
        """
        return self.chain[-1]
