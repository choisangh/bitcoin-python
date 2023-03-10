from .wallet import Wallet


class WalletManager:
    def __init__(self):
        self.wallets = []

    def create_wallet(self):
        wallet = Wallet()
        self.wallets.append(wallet)
        return wallet

    def get_wallet_by_public_key(self, public_key):
        for wallet in self.wallets:
            if wallet.public_key.to_string().hex() == public_key:
                return wallet
        return None



