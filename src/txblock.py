from blockchain import CBlock
from cryptography.hazmat.primitives import hashes
import random

class TxBlock (CBlock):

    block_reward = 25.0
    nonce = "AAAAAAA"
    leading_zeros = 2
    next_char_limit = 20
        
    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)
    
    def addTx(self, Tx_in):
        self.data.append(Tx_in)
    
    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False

        for tx in self.data:
            if not tx.is_valid():
                return False
            
        total_in, total_out = self.__count_totals()
        if total_out - total_in - self.block_reward > 0.000000000001:
            return False
        
        return True
    
    def good_nonce(self):
        # generate hash from block plus nonce - could be refactor from parent
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        this_hash =  digest.finalize()
       
        if this_hash[:self.leading_zeros] != bytes(''.join([ '\x4f' for i in range(self.leading_zeros)]),'utf8'):
            return False
        return int(this_hash[self.leading_zeros]) < self.next_char_limit

    def find_nonce(self):
        for i in range(1000000):
            self.nonce = ''.join([ 
                   chr(random.randint(0,255)) for i in range(10*self.leading_zeros)])
            if self.good_nonce():
                return self.nonce  
        return None

    def count_totals(self):
        total_in = 0
        total_out = 0
        
        for tx in self.data:
            for address, amount in tx.inputs:
                total_in += amount
            for address, amount in tx.outputs:
                total_out += amount
        
        return total_in, total_out

import signatures
from transactions import Tx
import pickle
import time
if __name__ == "__main__":
    pr1, pu1 = signatures.generate_keys()
    pr2, pu2 = signatures.generate_keys()
    pr3, pu3 = signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Sucess! Loaded tx is valid")
    loadfile.close()

    root = TxBlock(None)
    root.addTx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2,1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(pu3,1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)
    
    Tx4 = Tx()
    Tx4.add_input(pu1,1)
    Tx4.add_output(pu2, 1)
    Tx4.add_required(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)
    start = time.time()
    #print(B1.find_nonce())
    elapsed = time.time() - start
    print("elapsed time: " + str(elapsed) + " s.")
    if elapsed < 60:
        print("ERROR! Mining is too fast")
    if B1.good_nonce():
        print("Success! Nonce is good!")
    else:
        print("ERROR! Bad nonce")
    

