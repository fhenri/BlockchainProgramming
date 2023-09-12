'''
conftest.py or __init__.py
    import os
    import sys
    PROJECT_PATH = os.getcwd()
    SOURCE_PATH = os.path.join(
        PROJECT_PATH,"src"
    )
    sys.path.append(SOURCE_PATH)

running with `python -m unittest discover`
'''
import unittest

from blockchain import CBlock

class testClass:
    string = None
    num = 1264378
    def __init__(self, mystring):
        self.string = mystring
    def __repr__(self):
        return self.string + "---" + str(self.num)

class TestCBlock(unittest.TestCase):
    def compute_hash(self):
        root  = CBlock(b'root/genesis block', None)
        B1 = CBlock('child block', root)
        
        self.assertEqual(root.compute_hashh(), B1.previousHash)
        self.assertEqual(B1.previousBlock.compute_hash(), B1.previousHash)
        
    def test_is_valid(self):
        root  = CBlock(b'root/genesis block', None)
        B1 = CBlock('child block', root)
        B2 = CBlock('Im a brother', root)        
        B3 = CBlock(b'I contiain bytes', B1)
        B4 = CBlock(12354, B3)
        B5 = CBlock(testClass('Hi there!'), B4)
        B6 = CBlock("child of B5", B5)

        for b in [B1, B2, B3, B4, B5, B6]:
            self.assertTrue(b.is_valid())

    def test_tamper(self):
        root  = CBlock(b'root/genesis block', None)
        B1 = CBlock('child block', root)
        B2 = CBlock('Im a brother', root)        
        B3 = CBlock(b'I contiain bytes', B1)
        B4 = CBlock(12354, B3)
        B5 = CBlock(testClass('Hi there!'), B4)
        B6 = CBlock("child of B5", B5)

        B4.data = 12345
        self.assertFalse(B5.is_valid())
        
        B5.data.num = 23678
        self.assertFalse(B6.is_valid())

if __name__ == '__main__':
    unittest.main()
