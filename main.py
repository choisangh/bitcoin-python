from src.bitcoin.core import Blockchain
from src.bitcoin.core import Wallet
from src.bitcoin.core import Miner


if __name__ == '__main__':
    # Alice's Wallet
    alice_wallet = Wallet()
    alice_address = alice_wallet.public_key.to_string().hex()
    print("Alice's Address: ", alice_address)

    # Bob's Wallet
    bob_wallet = Wallet()
    bob_address = bob_wallet.public_key.to_string().hex()
    print("Bob's Address: ", bob_address)

    # Alice sends transaction to Bob
    transaction, signature = alice_wallet.send_transaction(bob_address, 5)
    print("Transaction Hash: ", transaction.calculate_hash())
    print("Transaction Signature: ", signature.hex())

    # 비트코인 노드 초기화
    blockchain = Blockchain()
    wallet = Wallet()
    miner = Miner(blockchain, wallet)
    print(wallet.get_public_key())
    # 채굴 시작
    print("채굴을 시작합니다...")
    while True:
        block = miner.mine()
        print(f"새로운 블록 채굴 완료: {block}")

