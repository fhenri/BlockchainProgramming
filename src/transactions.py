#Transaction.py
import signatures

class Tx:
    # list of input Addresses
    inputs  = None
    # list of output Addresses and amount
    outputs = None
    # list of signatures
    sigs = None
    # List of required signatures (multisigs)
    reqd = None
    
    # Initialize empty arrays
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
    
    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))
    
    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))
    
    def add_required(self, addr):
        self.reqd.append(addr)
    
    def sign(self, private):
        message = self.__gather()
        digest = signatures.sign(message, private)
        self.sigs.append(digest)
        
    def is_valid(self):
        message = self.__gather()

        total_in = 0
        for addr, amount in self.inputs:
            if amount < 0:
                return False
            total_in += amount

            found = False
            for s in self.sigs:
                if signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
            
        for key in self.reqd:
            found = False
            for s in self.sigs:
                if signatures.verify(message, s, key):
                    found = True
            if not found:
                return False

        total_out = 0
        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        if total_out > total_in:
            return False
        
        return True
    
    # Generate Private Method
    def __gather(self):
        return [
            self.inputs,
            self.outputs,
            self.reqd
        ]

    ## CBlock.compute_hash uses str(data) ie string representation 
    # of the Transaction so need to override the __repr__ function
    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "REQD:\n"
        for r in self.reqd:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr
