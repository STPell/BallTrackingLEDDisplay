import os
import SerialController
import time

a = SerialController.SerialController('/dev/ttyUSB0')
a.serial_socket.baudrate = 9600
a.serial_socket.writeTimeout = 0
a.open_serial()
time.sleep(3)

a.serial_socket.write("3,143,\n".encode('utf8'))
time.sleep(2)
a.serial_socket.flush()
time.sleep(10)
a.serial_socket.close()


