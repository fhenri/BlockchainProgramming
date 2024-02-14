import pickle
import socket
import server

import signatures
import transactions
import txblock

class Client:
    
    TCP_PORT = 5005

    def send_block(self, ip_addr, blk):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_addr, self.TCP_PORT))
        data = pickle.dumps(blk)
        s.send(data)
        s.close()
        return False


if __name__ == "__main__":
    pr1,pu1 = signatures.generate_keys()
    pr2,pu2 = signatures.generate_keys()
    pr3,pu3 = signatures.generate_keys()
    Tx1 = transactions.Tx()
    Tx1.add_input(pu1,2.3)
    Tx1.add_output(pu2,1.0)
    Tx1.add_output(pu3,1.1)
    Tx1.sign(pr1)

    Tx2 = transactions.Tx()
    Tx2.add_input(pu3,2.3)
    Tx2.add_input(pu2,1.0)
    Tx2.add_output(pu1,3.1)
    Tx2.sign(pr2)
    Tx2.sign(pr3)

    B1 = txblock.TxBlock(None)
    B1.addTx(Tx1)
    B1.addTx(Tx2)

    Client.send_block(Client, 'localhost', B1)

    Client.send_block(Client, 'localhost', Tx2)
