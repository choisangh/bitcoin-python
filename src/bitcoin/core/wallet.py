import binascii
import hashlib
import ecdsa
from .transaction import Transaction



class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate()  # 개인키 생성
        self.public_key = self.private_key.get_verifying_key()  # 공개키 생성
        self.balance = 0  # 계좌 잔액 설정

    def get_private_key(self):
        return binascii.hexlify(self.private_key.to_string()).decode('utf-8')

    def get_public_key(self):
        return binascii.hexlify(self.public_key.to_string()).decode('utf-8')

    def sign_transaction(self, message):
        signature = self.private_key.sign(message.encode())
        return binascii.hexlify(signature).decode('utf-8')

    def adjust_balance(self, amount):
        self.balance = amount

    @staticmethod
    def verify(public_key, message, signature):
        vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key))
        return vk.verify(binascii.unhexlify(signature), message.encode())

    def send_transaction(self, recipient_address, amount):
        from .globals import TRANSACTION_POOL
        # TODO : UTXO 방식으로 변경
        if self.balance < amount:
            print(f"잔액 부족 {self.balance}")
            return None
        transaction = Transaction(self.public_key.to_string().hex(), self.private_key, recipient_address, amount)
        signature = transaction.sign_transaction()

        TRANSACTION_POOL.add_transaction(transaction)
        return transaction, signature

