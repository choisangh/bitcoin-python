import hashlib
import json
from time import time
from .transaction import Transaction
from .block import Block
from .globals import WALLET_MANAGER


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # 제네시스 블록 생성
        self.new_block(previous_hash=1, nonce=100)

    def new_block(self, nonce, previous_hash=None):
        block = Block(height=len(self.chain)+1,
                      transactions=self.current_transactions,
                      nonce=nonce,
                      previous_hash=previous_hash or self.hash(self.chain[-1]))
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, sender_private_key, recipient, amount, coinbase):
        transaction = Transaction(sender, sender_private_key, recipient, amount)
        self.current_transactions.append(transaction.to_dict())
        self.adjust_balances(transaction, coinbase)
        return self.last_block.height + 1

    def adjust_balances(self, transaction, coinbase):
        # TODO : UTXO 방식으로 변경
        # 블록 내 트랜잭션에서 송신 계좌와 수신 계좌의 주소와 금액을 추출
        sender_wallet = WALLET_MANAGER.get_wallet_by_public_key(transaction.sender_address)
        recipient_wallet = WALLET_MANAGER.get_wallet_by_public_key(transaction.recipient_address)
        amount = transaction.amount
        if coinbase is False:
            # 송신 계좌의 잔액을 변경
            sender_wallet.adjust_balance(sender_wallet.balance - amount)

        # 수신 계좌의 잔액을 변경
        recipient_wallet.adjust_balance(recipient_wallet.balance + amount)
        print('수신완료')


    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
