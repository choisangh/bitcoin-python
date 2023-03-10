class TransactionPool:
    def __init__(self):
        self.pool = []

    def add_transaction(self, transaction):
        self.pool.append(transaction)
    
    # TODO: 블록 채굴 시 검증된 트랙잭션을 트랜잭션 풀에서 제거하는 로직

