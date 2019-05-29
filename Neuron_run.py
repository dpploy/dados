from rs_232 import RS_232
from neuron import Neuron
import time

rs = RS_232(wrk_dir='/tmp/Cortix',filename='ir_7040')
neuron = Neuron(task=rs.ir_7040,wrk_dir='/tmp/Cortix',name='ir_7040')

while True:
    line = neuron.read_line()
    print(line)
    time.sleep(0.5)
input("End?")
