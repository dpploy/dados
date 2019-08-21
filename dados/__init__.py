#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dados_main import Dados
from dados.devices.IR_7040 import IR_7040
try:
    from dados.devices.mcc_118 import MCC_118
except ModuleNotFoundError as e:
    'DAQHats library not installed'
    pass
