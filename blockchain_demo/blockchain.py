"""
DOCSTRING
"""
import hashlib
import time

GENESIS_INDEX = 0
GENESIS_PREVIOUS_HASH = '0'
GENESIS_TIMESTAMP = 1495851743
GENESIS_DATA = 'first block'

class Block():
    """
    DOCSTRING
    """
    def __init__(self, params):
        self.index = params.index
        self.previous_hash = params.previous_hash
        self.timestamp = params.timestamp
        self.data = params.data
        self.hash = self.calc_hash()

    def calc_hash(self):
        return hashlib.sha256(str(self.params()).encode()).hexdigest()

    @classmethod
    def genesis_block(cls):
        params = BlockParams.genesis_params()
        return cls(params)

    def has_valid_hash(self):
        return self.calc_hash() == self.hash

    def has_valid_index(self, previous_block):
        return self.index == previous_block.index + 1

    def has_valid_previous_hash(self, previous_block):
        return self.previous_hash == previous_block.hash

    def params(self):
        return BlockParams(
            self.index,
            self.previous_hash,
            self.timestamp,
            self.data)

class BlockChain():
    """
    DOCSTRING
    """
    def __init__(self):
        self.blockchain_store = self.fetch_blockchain()

    def fetch_blockchain(self):
        return [Block.genesis_block()]
    
    def generate_next_block(self, data):
        """
        DOCSTRING
        """
        index = len(self.blockchain_store)
        previous_hash = self.latest_block().hash
        timestamp = int(time.time())
        params = BlockParams(index, previous_hash, timestamp, data)
        new_block = Block(params)
        self.blockchain_store.append(new_block)

    def latest_block(self):
        return self.blockchain_store[-1]
    
    def receive_new_block(self, new_block):
        """
        DOCSTRING
        """
        previous_block = self.latest_block()
        if not new_block.has_valid_index(previous_block):
            print('invalid index')
            return
        if not new_block.has_valid_previous_hash(previous_block):
            print('invalid previous hash')
            return
        if not new_block.has_valid_hash():
            print('invalid hash')
            return
        self.blockchain_store.append(new_block)

class BlockParams:
    """
    DOCSTRING
    """
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data

    def __str__(self):
        return str(self.index) + self.previous_hash + str(self.timestamp) + self.data

    @classmethod
    def genesis_params(cls):
        return cls(GENESIS_INDEX, GENESIS_PREVIOUS_HASH, GENESIS_TIMESTAMP, GENESIS_DATA)
