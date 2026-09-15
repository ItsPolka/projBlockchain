import hashlib
import json
from time import time

"""
Code provided by:   @katakakikita
https://medium.com/@katakakikita/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03
"""

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        pass

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        pass

    @staticmethod
    def hash(block):
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