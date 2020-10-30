from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import requests
import sys
import uuid
import threading
import time

class Bitpole_RPC:
    def __init__(self): pass

    def batch_(self, commands):
        response = []
        for command in commands:
            res = requests.post("https://w.bitpole.org/api/v1/rpc_execute", json={"command": " ".join(command)}).json()
            response.append(res["response"] if res["status"] else False)

        return response

class Client:
    def log(self, text): print(f"[Client] {text}")

    def debug(self, text):
        if self.debug_enabled:
            print(f"[sync.Client ~ debug] {text}")

    def __init__(self, node=None, debug=False):
        self.node_addr = node
        self.debug_enabled = debug
        self.connected = False

        self.rpc_daemon_polling = False

    def get_rpc(self, node=None):
        self.node_addr = node or self.node_addr

        if self.node_addr:
            if "://" not in self.node_addr:
                self.node_addr = f"http://{self.node_addr}"

        if self.node_addr:
            return AuthServiceProxy(f"{self.node_addr}")
        else:
            return Bitpole_RPC()

    def rpc_execute(self, commands):
        if type(commands) == str: commands = [commands]

        self.debug(f"> {sys.getsizeof(commands)}")

        try:
            res = self.get_rpc().batch_([command.split(" ") for command in commands])
        except JSONRPCException as e:
            self.debug(f"Error [{e}] (caused by pybitcoinrpc.Client.rpc_execute)")
            return [False for x in commands]

        self.debug(f"< {sys.getsizeof(res)}")

        return res

    def __rpc_daemon_polling__(self):
        self.debug("RPC Daemon polling started")

        while True:
            with self.lock:
                commands_package = [{"fetch_id": c, "fetch_command": self.commands_buffer[c]["command"]} for c in self.commands_buffer if self.commands_buffer[c]["status"] == "created"]

            if not commands_package:
                continue

            response = self.rpc_execute([c["fetch_command"] for c in commands_package])

            with self.lock:
                for i, c in enumerate(commands_package):
                    self.commands_buffer[c["fetch_id"]]["response"] = response[i]
                    self.commands_buffer[c["fetch_id"]]["status"] = "completed"

            time.sleep(0.05)

    def rpc_daemon(self):
        self.rpc_daemon_polling = True

        self.lock = threading.Lock()
        self.commands_buffer = {}

        self.debug("Preparing to launch daemon")

        self.rpc_commands_polling_thread = threading.Thread(target=self.__rpc_daemon_polling__, args=[])
        self.rpc_commands_polling_thread.daemon = True
        self.rpc_commands_polling_thread.start()

    def rpc_fetch(self, command):
        if not self.rpc_daemon_polling:
            self.rpc_daemon()

        fetch_id = f"{uuid.uuid4()}"

        with self.lock:
            self.commands_buffer[fetch_id] = {
                "command": command,
                "status": "created"
            }

        while self.commands_buffer[fetch_id]["status"] != "completed":
            time.sleep(0.05)

        with self.lock:
            res = self.commands_buffer[fetch_id] if self.commands_buffer[fetch_id]["status"] == "completed" else False
            del self.commands_buffer[fetch_id]

        return res["response"]
