from cryptography.hazmat.primitives import hashes

class CBlock:
    previousHash = None
    previousBlock = None
    data = None
    
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.compute_hash()
                 
    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        return digest.finalize()
    
    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.compute_hash() == self.previousHash