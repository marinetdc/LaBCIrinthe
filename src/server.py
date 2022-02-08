import socket

LOCALHOST = '127.0.0.1'
PORT = 8000


class Server:
    """
    This class serves as the host for the server connection with Android app. It accepts datastream in the format of str and converts into a 3D vector of floats.
    This class is currently very unstable.
    
    """
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.ip = "0.0.0.0"  # connect through external connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('host name is: ' + self.host)
        print('host IP is: ' + self.ip)

    def start(self):
        self.socket.bind((self.ip, self.port))
        print('Server started')
        self.socket.listen(5)

    def get(self):
        client, addr = self.socket.accept()
        data_str = client.recv(1024).decode("utf-8")
        if data_str != '' and not None:
            acc_vect = data_str.split(sep=',')
            try:
                acc_vect = [float(x) for x in acc_vect]
            except ValueError:
                print("Oops!")

            return acc_vect


if __name__ == '__main__':
    server = Server(PORT)
    server.start()
    while True:
        vector = server.get()
        print(vector)
