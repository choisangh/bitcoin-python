import hashlib
import json
from .globals import DIFFICULTY_TARGET


class Miner:
    def __init__(self, blockchain, wallet):
        self.blockchain = blockchain
        self.wallet = wallet

    def mine(self):
        last_block = self.blockchain.last_block
        last_proof = last_block.block_header.nonce
        proof = self.proof_of_work(last_proof)
        # TODO: 트랜잭션 풀에서 트랜잭션 선정 및 POW 적용 로직

        # 보상 트랜잭션 생성
        self.blockchain.new_transaction(
            sender='coinbase',
            sender_private_key='',
            recipient=self.wallet.get_public_key(),
            amount=1,
            coinbase=True
        )

        previous_hash = self.blockchain.hash(last_block.to_dict())
        block = self.blockchain.new_block(proof, previous_hash)

        return block

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof, difficulty_target=DIFFICULTY_TARGET) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, difficulty_target):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty_target] == "0" * difficulty_target
