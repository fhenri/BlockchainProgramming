import pickle
import socket

class Server:
    
    TCP_PORT = 5005
    BUFFER_SIZE=1024

    def open_connection(self, ip_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, self.TCP_PORT))
        s.listen()
        return s

    def receive_object(self, socket):
        new_sock,addr = socket.accept()
        all_data = b''
        while True:
            data = new_sock.recv(self.BUFFER_SIZE)
            if not data: break
            all_data = all_data + data
        return pickle.loads(all_data)

if __name__ == "__main__":
    s = Server.open_connection(Server, 'localhost')
    newB = Server.receive_object(Server, s)
    print (newB.data[0])
    print (newB.data[1])
    if (newB.is_valid()):
        print ("Success. Tx is valid")
    else:
        print ("Error. Tx invalid.")
    if newB.data[0].inputs[0][1] == 2.3:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[0].outputs[1][1] == 1.1:
        print ("Success. Output value matches")
    else:
        print ("Error! Wrong output value for block 1, tx 1")
    if newB.data[1].inputs[0][1] == 2.3:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[1].inputs[1][1] == 1.0:
        print ("Success. Input value matches")
    else:
        print ("Error! Wrong input value for block 1, tx 1")
    if newB.data[1].outputs[0][1] == 3.1:
        print ("Success. Output value matches")
    else:
        print ("Error! Wrong output value for block 1, tx 1")
    newTx= Server.receive_object(Server, s)
    print (newTx)
         
