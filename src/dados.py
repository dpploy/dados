import threading, datetime, time, os
import numpy as np
from cortix.src.module import Module
from cortix.src.cortix_main import Cortix
from cortix.src.port import Port
from src.rs_232 import RS_232
from src.mcc_118 import MCC_118
from src.plotting import Plot

class Dados(Module):
    def __init__(self):
        self.cortix = Cortix()
        self.rs232 = RS_232()
        self.mcc118 = MCC_118()
        self.plot = Plot()
    def run(self):
        p1 = Port('rs')
        p2 = Port('mcc')
        p3 = Port('plot')

        p1.connect(p3)
        p2.connect(p3)

        self.rs232.add_port(p1)
        self.mcc118.add_port(p2)
        self.plot.add_port(p3)

        self.cortix.add_module(self.rs232)
        self.cortix.add_module(self.mcc118)
        self.cortix.add_module(self.plot)

        self.cortix.run()

if __name__=='__main__':
    app = Dados()
    app.run()
