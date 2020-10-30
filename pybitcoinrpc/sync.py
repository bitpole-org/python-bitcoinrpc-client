from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys

class Client:
    def log(self, text): print(f"[Client] {text}")

    def debug(self, text):
        if self.debug:
            print(f"[sync.Client ~ debug] {text}")

    def __init__(self, node=None, debug=False):
        self.node_addr = node
        self.debug = debug
        self.connected = False

    def get_rpc(self, node=None):
        self.node_addr = node or self.node_addr
        self.connected = True

        self.node_addr = self.node_addr.replace("http://", "").replace("https://", "") \
            if "://" in self.node_addr else self.node_addr

        return AuthServiceProxy(f"http://{self.node_addr}")

    def get_best_block_hash(self): return self.get_rpc().getbestblockhash()
    def get_blockchain_info(self): return self.get_rpc().getblockchaininfo()
    def list_received_by_address(self, count): return self.get_rpc().listreceivedbyaddress(count)

    def rpc_command(self, command):
        self.debug(f"> {sys.getsizeof(command)}")
        res = self.get_rpc().batch_(command.split(" "))
        self.debug(f"< {sys.getsizeof(res)}")
        return res
