from polarisercontrol import *
from data_processing import *
import numpy as np

send_command("G1 X120 Z51 F300")
movepolariser(45)