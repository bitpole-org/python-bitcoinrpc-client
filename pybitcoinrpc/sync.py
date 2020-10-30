from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class Client:
    def log(self, text): print(f"[Client] {text}")

    def debug(self, text):
        if self.debug:
            print(f"[sync.Client ~ debug] {text}")

    def __init__(self, node=None, debug=False):
        self.node_addr = node
        self.debug = debug
        self.connected = False

    def connect(self, node=None):
        self.node_addr = node or self.node_addr
        self.connected = True

        self.node_addr = self.node_addr.replace("http://", "").replace("https://", "")

        self.rpc_connection = AuthServiceProxy(f"http://{self.node_addr}")

    def getbestblockhash(self):
        if not connected: raise Exception("Connect to bitcoin node")
