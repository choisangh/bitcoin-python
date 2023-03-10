import json
import hashlib
import time
import binascii
import ecdsa
from .__version__ import __version__


class Input:
    def __init__(self, transaction_hash, output_index,
                 unlocking_script_size, unlocking_script, sequence_number):
        self.transaction_hash = transaction_hash
        self.output_index = output_index
        self.unlocking_script_size = unlocking_script_size
        self.unlocking_script = unlocking_script
        self.sequence_number = sequence_number


class Output:
    def __init__(self, amount,
                 locking_script_size, locking_script):
        self.amount = amount
        self.locking_script_size = locking_script_size
        self.locking_script = locking_script


class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.version = __version__
        self.number_of_inputs = None
        self.inputs = None
        self.number_of_outputs = None
        self.outputs = None
        self.Locktime = None

        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

    def to_dict(self):
        return {
            'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    def calculate_hash(self):
        """
        트랜잭션 해싱
        :return:
        """
        transaction = self.to_dict()
        transaction_string = json.dumps(transaction, sort_keys=True).encode('utf-8')
        return hashlib.sha256(transaction_string).hexdigest()

    def sign_transaction(self):
        """
        비밀키 사인 매서드
        :return:
        """
        hash = self.calculate_hash()
        signature = self.sender_private_key.sign(hash.encode())  # 개인키를 사용하여 트랜잭션 해시 서명
        self.signature = binascii.hexlify(signature).decode('utf-8')  # 서명 값 디코딩
        return self.signature

    def is_valid(self):
        """
        서명값 검증 매서드
        :return:
        """
        public_key = ecdsa.VerifyingKey.from_string(binascii.unhexlify(self.sender_address))
        hash = self.calculate_hash().encode()
        return public_key.verify(binascii.unhexlify(self.signature), hash)
