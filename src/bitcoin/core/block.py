from time import time
import hashlib
from .__version__ import __version__
import json
from .globals import DIFFICULTY_TARGET


class BlockHeader:
    def __init__(self, previous_hash, merkleroot, difficultytarget, nonce):
        self.version = __version__
        self.previous_block_hash = previous_hash
        self.merkle_root = merkleroot
        self.timestamp = time()
        self.difficulty_target = difficultytarget
        self.nonce = nonce

    def to_dict(self):
        return {
            "version": self.version,
            "previous_block_hash": self.previous_block_hash,
            "merkle_root": self.merkle_root,
            "timestamp": time(),
            "difficulty_target": self.difficulty_target,
            "nonce": self.nonce
        }


class Block:
    def __init__(self, height, transactions, nonce, previous_hash):
        previous_hash = previous_hash or self.hash(self.chain[-1])
        self.block_header = BlockHeader(previous_hash=previous_hash,
                                        merkleroot=self.get_merkle_tree(transactions),
                                        difficultytarget=DIFFICULTY_TARGET,
                                        nonce=nonce)
        self.height = height
        self.transactions = transactions
        self.block_size = None

    def to_dict(self):
        return {
            'block_header': self.block_header.to_dict(),
            'height': self.height,
            'transactions': self.transactions,
            'transaction_counter': len(self.transactions),
            'block_size': self.block_size
        }

    @staticmethod
    def get_merkle_tree(txns):
        if len(txns) == 0:
            return [None]

        if len(txns) % 2 != 0:
            txns.append(txns[-1])

        tree = [hashlib.sha256(hashlib.sha256(json.dumps(txn, sort_keys=True).encode()).digest()).hexdigest()
                for txn in txns]

        while len(tree) > 1:
            if len(tree) % 2 != 0:
                tree.append(tree[-1])
            tree = [hashlib.sha256((tree[i] + tree[i + 1]).encode()).hexdigest() for i in range(0, len(tree), 2)]

        return tree[0]

    def get_merkle_path(self, txns, index):
        path = []
        merkle_tree = self.get_merkle_tree(txns)
        if index >= len(txns):
            return path

        current = index
        for level in range(len(merkle_tree)):
            if current % 2 == 0:
                sibling = current + 1
            else:
                sibling = current - 1
            path.append(merkle_tree[sibling])
            current = current // 2
        return path

