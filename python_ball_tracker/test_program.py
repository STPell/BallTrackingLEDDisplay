import SerialController as sc
import os
import time

a = sc.SerialController('COM4')
a.open_serial()
time.sleep(3)

a.write_data([4,2,3,1])

a.serial_socket.flush()
a.close_serial()
