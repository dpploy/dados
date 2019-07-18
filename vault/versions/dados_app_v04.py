import os, sys, time
import socket,  threading
sys.path.append("../..")
from rs_232 import RS_232
from neuron import Neuron

class DadosApp:
    def __init__(self):
        self.rs = RS_232(wrk_dir='/tmp/Cortix',filename='ir_7040')
        self.neuron = Neuron(task=self.rs.ir_7040,wrk_dir='/tmp/Cortix',name='ir_7040')\

        self.socket_list=[]
        self.init_port=60000
        self.port=60001
        #self.host= str(socket.gethostbyname(socket.gethostname()))
        self.host= '10.253.90.99'
        print(self.host)

    def start_server(self):
        oldline=''
        while True:
            line = self.neuron.read_line()
            if line == oldline:
                time.sleep(0.1)
                continue
            oldline=line
            print(line)
            padding=line
            padding += (" "*(250-len(padding)))
            c=0
            for conn in self.socket_list:
                try:
                    conn.send(padding.encode())
                except Exception as e:
                    print(e)
                    conn.close()
                    del self.socket_list[c]
                c+=1
            if 'init_worker' not in [f.name for f in threading.enumerate()]:
                worker=threading.Thread(target=self.initialize_socket, name='init_worker')
                worker.daemon=True
                worker.start()
    def initialize_socket(self):
        try:
            print('initial socket')
            sock=socket.socket()
            sock.settimeout(60)
            sock.bind((self.host,self.init_port))
            sock.listen(5)
            conn,addr=sock.accept()
            self.port+=1
            string='port, {}, host, {}'.format(self.port,self.host)
            string+=' '*(40-len(string))
            for n in range(2):
                conn.send(string.encode())
                time.sleep(0.5)
            print('Socket Initialized!')
            conn.close()
            s = socket.socket()
            s.settimeout(60)
            print(self.port)
            s.bind((self.host, self.port))
            s.listen(5)
            conn, addr = s.accept()
            self.socket_list.append(conn)
            print('Connected to:{},{}'.format(conn,addr))
        except Exception as e:
                return
        return
    def exit():
        for conn in self.socket_list:
            conn.close()
        return

if __name__=='__main__':
    app = DadosApp()
    app.start_server()
