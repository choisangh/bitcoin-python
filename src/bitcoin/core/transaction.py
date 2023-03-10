import json
import hashlib
import time

class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def calculate_hash(self):
        transaction = {
            'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        transaction_string = json.dumps(transaction, sort_keys=True).encode('utf-8')
        return hashlib.sha256(transaction_string).digest()

    def sign_transaction(self):
        hash = self.calculate_hash()
        signature = self.sender_private_key.sign(hash)
        return signature

    def sign(self, private_key):
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        self.signature = private_key.sign(message)

    def is_valid(self):
        public_key = self.sender.get_public_key()
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        return public_key.verify(self.signature, message)
