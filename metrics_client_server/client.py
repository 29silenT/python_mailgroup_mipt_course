import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metric, value, timestamp=int(time.time())):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                res = sock.sendall(" ".join(["put", metric, str(value), str(timestamp) + "\n"]).encode('utf-8'))
                resp = sock.recv(1024).decode('utf-8').split('\n')
                if resp[0] is 'error':
                    raise ClientError("Custom Client Error (send put)")
                elif res is None and resp[0] is 'ok':
                    return res

            except socket.error:
                raise ClientError("Custom Socket Error (put)")

    def get(self, metric):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                res = sock.sendall(" ".join(["get", metric + "\n"]).encode('utf-8'))
                if res is None:
                    data = sock.recv(1024).decode('utf-8')
                    if data[:3] == "ok\n" and data[-1:] == "\n":
                        value = data[3:-2]
                        if len(value) > 1:
                            d = {}
                            for i in value.split("\n"):
                                k = i.split()[0]
                                v2 = int(i.split()[2])
                                v1 = float(i.split()[1])
                                if k not in d:
                                    d[k] = [(v2, v1)]
                                else:
                                    d[k].append((v2, v1))
                                    d[k].sort(key=lambda tup: tup[0])
                            return d
                        else:
                            return {}
                    else:
                        raise ClientError("Custom Client Error (receive)")
                else:
                    raise ClientError("Custom Client Error (send)")
            except socket.error:
                raise ClientError("Custom Socket Error (get)")


class ClientError(Exception):
    pass

