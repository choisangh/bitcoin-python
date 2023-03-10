import hashlib
import json


class Miner:
    def __init__(self, blockchain, wallet):
        self.blockchain = blockchain
        self.wallet = wallet

    def mine(self):
        last_block = self.blockchain.last_block
        last_proof = last_block['nonce']
        proof = self.proof_of_work(last_proof)

        # 보상 트랜잭션 생성
        self.blockchain.new_transaction(
            sender='coinbase',
            recipient=self.wallet.get_public_key(),
            amount=1
        )

        # TODO : 트랜 잭션 추가

        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)

        return block

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
