import datetime, socket, time


class Receiver:
    def __init__(self):
        print('starting Receiver')
        s = socket.socket()
        host = '10.253.90.99'
        port = 60000
        s.connect((host, port))
        data = s.recv(40).decode().split(', ')
        self.port=int(data[1])
        self.host=data[3].strip()
        s.close()
        print(self.port,self.host)
        time.sleep(3)
        self.s = socket.socket()
        socket.getaddrinfo('127.0.0.1', 8080)
        self.s.connect((self.host, self.port))
    def run(self,conn):
        print('run')
        self.conn = conn
        print(self.conn)
        while True:
            print('hi')
            self.data = self.s.recv(400)
            self.line = self.data.decode().strip()
            print(self.line)
            self.conn.send(self.line)
if __name__ == "__main__":
    app = Receiver()
    app.run('i')
