from src.bitcoin.core import Blockchain
from src.bitcoin.core import WALLET_MANAGER
from src.bitcoin.core import Miner



if __name__ == '__main__':


    # Bob's Wallet
    bob_wallet = WALLET_MANAGER.create_wallet()
    bob_address = bob_wallet.public_key.to_string().hex()
    print("Bob's Address: ", bob_address)

    # 비트코인 노드 초기화
    blockchain = Blockchain()
    miner = Miner(blockchain, bob_wallet)
    # 채굴 시작
    print("채굴을 시작합니다...")
    for i in range(10):
        block = miner.mine()
        print(f"새로운 블록 채굴 완료: {block.to_dict()}")
    print(bob_wallet.balance)
    # Alice's Wallet
    alice_wallet = WALLET_MANAGER.create_wallet()
    alice_address = alice_wallet.public_key.to_string().hex()
    print("Alice's Address: ", alice_address)
    # Alice sends transaction to Bob
    transaction, signature = bob_wallet.send_transaction(alice_address, 5)
    print("Transaction Hash: ", transaction.calculate_hash())
    print("Transaction Signature: ", signature)
    print(alice_address)

    print("Bob's wallet balance: ", bob_wallet.balance)
    print("Alice's wallet balance: ", alice_wallet.balance)



