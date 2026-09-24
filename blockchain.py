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
    def __init__(self, difficulty: int):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.difficulty = difficulty

    def new_block(self, transaction):
        previous_hash = self.last_block.hash if self.chain else "0"
        nblock = Block(len(self.chain), transaction, previous_hash)
        success = nblock.mine_block(self.difficulty, self)
        if success:
            self.chain.append(nblock)
            return nblock
        return None

    @property
    def last_block(self) -> Block:
        """
        Returns the last Block in the chain
        """
        return self.chain[-1]

def main():
    blockchain = Blockchain(4)
    blockchain.new_block("Alice le manda 1BTC a Bob")
    print(blockchain.last_block)

if __name__ == "__main__":
    main()