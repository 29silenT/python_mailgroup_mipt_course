import asyncio


class ClientServerProtocol(asyncio.Protocol):
    _db = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if ClientServerProtocol.check_data(data):
            msg = data.split()
            if msg[0] == 'put':
                return self.put(msg[1], float(msg[2]), int(msg[3]))

            elif msg[0] == 'get':
                return self.get(msg[1])

        else:
            return 'error\nwrong command\n\n'

    def put(self, key, value, timestamp):
        if key not in ClientServerProtocol._db:
            ClientServerProtocol._db[key] = []
        if (value, timestamp) not in ClientServerProtocol._db[key]:
            ClientServerProtocol._db[key].append((value, timestamp))
        return 'ok\n\n'

    def get(self, key):
        if key in ClientServerProtocol._db:
            res = 'ok\n'
            for item in ClientServerProtocol._db[key]:
                res += " ".join([key, str(item[0]), str(item[1]) + "\n"])
            return res + '\n'

        elif key == '*':
            res = 'ok\n'
            for key, item in ClientServerProtocol._db.items():
                for i in item:
                    res += " ".join([key, str(i[0]), str(i[1]) + "\n"])
            return res + '\n'

        else:
            return 'ok\n\n'

    @staticmethod
    def check_data(data):
        msg = data.split()
        if msg[0] == 'put':
            if len(msg) == 4:
                if ClientServerProtocol.isfloat(msg[2]) and msg[3].isdigit() and data[-1:] == '\n':
                    return True
                else:
                    return False
            else:
                return True

        elif msg[0] == 'get':
            if len(msg) == 2 and data[-1:] == '\n':
                return True
            else:
                return False

        else:
            return False

    @staticmethod
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 8888)
