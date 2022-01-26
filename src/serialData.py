import serial
#from threading import Thread

def readSerialData(port):
    ###waits for a value to be sent
    for i in range(1):
        ser = serial.Serial('COM5')
        ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    return decoded_bytes

class readLine:
    """
    pyserial object wrapper for reading line
    source: https://github.com/pyserial/pyserial/issues/216
    """
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)
