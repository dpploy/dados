import datetime, socket, time
from cortix.src.module import Module


class Receiver(Module):
    def __init__(self):
        super().__init__()

        # Number of lines to send
        self.num_data = 1000

        # If True, send dummy data without connecting to the pi
        self.debug = True

        # Otherwise, connect to the Pi
        if not self.debug:
            s = socket.socket()
            host = 'xx.xxx.xx.xx'
            port = 60000
            s.connect((host, port))
            data = s.recv(40).decode().split(', ')
            self.port=int(data[1])
            self.host=data[3].strip()
            s.close()
            self.s = socket.socket()
            self.s.connect((host, port))

    def run(self):
        i = 0
        while i < self.num_data:
            if self.debug:
                # Send dummy data
                data = "P1, 1289Od, 1.23e-2, 2.07e-2, 2.87e-2, 6.35e-2,\
                        0.00e+0, 0.00e+0, 67}, 2019-03-19 11:55:00".encode()
            else:
                # Send real data
                data = s.recv(400)

            # Grab the values from the comma separated string
            values = data.decode().strip().split(",")

            # Send the third value to DataPlot along with the current time step
            self.send((i, values[2]), 'serial')

            i+= 1
        self.send("DONE", "serial")
