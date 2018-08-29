import threading
import serial
import subprocess

DATA_FORMAT = "{},{},{},{}\n"
ENCODING = "utf8"

class SerialController:
    baud = 9600
    stop_bit = 1
    parity = 'N'
    is_open = False

    def __init__(self, port):
        self.serial_socket = serial.Serial()
        self.serial_socket.setPort(port)
        self.serial_socket.baud = self.baud
        self.serial_socket.stopbits = self.stop_bit
        self.serial_socket.parity = self.parity

        self.socket_lock = threading.Lock()


    def open_serial(self):
        self.is_open = True
        self.serial_socket.open()


    def close_serial(self):
        self.is_open = False
        self.socket_lock.acquire() #wait for the lock to access serial socket
        self.serial_socket.close()


    def write_data(self, *data_to_write):
        data = DATA_FORMAT.format(*data_to_write)
        if self.is_open:
            threading.Thread(target=self._multi_thread_safe_send,
                        kwargs={"data":data, "lock":self.socket_lock}).start()


    def _multi_thread_safe_send(self, **kwargs):
        to_send = kwargs["data"]
        lock = kwargs["lock"]
        lock.acquire()
        self.serial_socket.write(bytes(to_send, ENCODING))
        self.serial_socket.flush()
        lock.release()

