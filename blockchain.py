import hashlib
import json
from time import time

"""
Code provided by:   @katakakikita
https://medium.com/@katakakikita/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03
"""

class Blockchain:
    def __init__(self):
        self.index=index
        self.timestamp=timestamp
        self.transaction=transaction
        self.previous_hash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, index,timestamp,transaction,previousHash,nonce):


        pass


    @staticmethod
    def calculateHash(block):
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