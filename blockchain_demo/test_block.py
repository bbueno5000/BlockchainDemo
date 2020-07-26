import unittest
from .. import block
from .. import block_params


class TestBlock(unittest.TestCase):

    def test_has_valid_index(self):
        prev_block = create_block(0, '0', 1, 'first_block')

        with self.subTest('valid index'):
            new_block = create_block(1, '0', 1, 'second block')
            self.assertTrue(new_block.has_valid_index(prev_block))

        with self.subTest('invalid index'):
            new_block = create_block(2, '0', 1, 'second block')
            self.assertFalse(new_block.has_valid_index(prev_block))

    def test_has_valid_previous_hash(self):
        prev_block = create_block(0, '0', 1, 'first_block')
        prev_hash = prev_block.hash

        with self.subTest('valid previous hash'):
            new_block = create_block(1, prev_hash, 1, 'second block')
            self.assertTrue(new_block.has_valid_previous_hash(prev_block))

        with self.subTest('invalid previous hash'):
            new_block = create_block(2, '0', 1, 'second block')
            self.assertFalse(new_block.has_valid_previous_hash(prev_block))

    def test_has_valid_hash(self):
        with self.subTest('valid hash'):
            new_block = create_block(1, '0', 1, 'second block')
            self.assertTrue(new_block.has_valid_hash())

        with self.subTest('invalid hash'):
            new_block = create_block(2, '0', 1, 'second block')
            new_block.hash = 'invalidhash'
            self.assertFalse(new_block.has_valid_hash())


def create_block(index, previous_hash, timestamp, data):
    params = block_params.BlockParams(
        index, previous_hash, timestamp, data)
    return block.Block(params)

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import MagicMock
from .. import blockchain


class TestBlockChain(unittest.TestCase):

    def test_generate_new_block(self):
        bc = blockchain.BlockChain()
        old_bc_length = len(bc.blockchain_store)

        data = 'this is new block'

        with self.subTest('add new block to blockchain'):
            bc.generate_next_block(data)
            self.assertEqual(len(bc.blockchain_store) - old_bc_length, 1)
            self.assertEqual(bc.latest_block().data, data)

    def test_receive_blockchain(self):
        bc = blockchain.BlockChain()
        old_bc_lengh = len(bc.blockchain_store)

        prev_block = MagicMock()
        new_block = MagicMock()
        with self.subTest('valid block should be added to blockchain'):
            new_block.has_valid_index = MagicMock(return_value=True)
            new_block.has_valid_previous_hash = MagicMock(return_value=True)
            new_block.has_valid_hash = MagicMock(return_value=True)

            bc.blockchain_store = [prev_block]
            bc.receive_new_block(new_block)
            self.assertEqual(len(bc.blockchain_store) - old_bc_lengh, 1)

        with self.subTest('invalid block shoud not be added to blockchain'):
            new_block.has_valid_index = MagicMock(return_value=False)
            new_block.has_valid_previous_hash = MagicMock(return_value=False)
            new_block.has_valid_hash = MagicMock(return_value=False)

            bc.blockchain_store = [prev_block]
            bc.receive_new_block(new_block)
            self.assertEqual(len(bc.blockchain_store) - old_bc_lengh, 0)



