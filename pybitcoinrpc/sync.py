from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys

class Client:
    def log(self, text): print(f"[Client] {text}")

    def debug(self, text):
        if self.debug_enabled:
            print(f"[sync.Client ~ debug] {text}")

    def __init__(self, node=None, debug=False):
        self.node_addr = node
        self.debug_enabled = debug
        self.connected = False

    def get_rpc(self, node=None):
        self.node_addr = node or self.node_addr

        if "://" not in self.node_addr:
            self.node_addr = f"http://{self.node_addr}"

        return AuthServiceProxy(f"{self.node_addr}")

    def get_best_block_hash(self): return self.get_rpc().getbestblockhash()
    def get_blockchain_info(self): return self.get_rpc().getblockchaininfo()

    def rpc_fetch(self, commands):
        self.debug(f"> {sys.getsizeof(commands)}")
        res = self.get_rpc().batch_([command.split(" ") for command in commands])
        self.debug(f"< {sys.getsizeof(res)}")
        return res
