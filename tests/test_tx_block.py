import pickle
import signatures
from txblock import TxBlock
from transactions import Tx

class TestTXBlock:
    def test_transaction(self):
        pr1, pu1 = signatures.generate_keys()
        pr2, pu2 = signatures.generate_keys()
        pr3, pu3 = signatures.generate_keys()

        Tx1 = Tx()
        Tx1.add_input(pu1, 1)
        Tx1.add_output(pu2, 1)
        Tx1.sign(pr1)

        assert Tx1.is_valid()

        savefile = open("tests/data/tx.dat", "wb")
        pickle.dump(Tx1, savefile)
        savefile.close()

        loadfile = open("tests/data/tx.dat", "rb")
        newTx = pickle.load(loadfile)

        assert newTx.is_valid()
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

        assert B1.is_valid()
        savebfile = open("tests/data/block.dat", "wb")
        pickle.dump(B1, savebfile)
        savebfile.close()

        loadbfile = open("tests/data/block.dat" ,"rb")
        load_B1 = pickle.load(loadbfile)
        
        loadbfile.close()
        assert load_B1.previousBlock.is_valid()
        assert load_B1.is_valid()

        for b in [root, B1, load_B1, load_B1.previousBlock]:
            assert b.is_valid()

        B2 = TxBlock(B1)
        Tx5 = Tx()
        Tx5.add_input(pu3, 1)
        Tx5.add_output(pu1, 100)
        Tx5.sign(pr3)
        B2.addTx(Tx5)

        load_B1.previousBlock.addTx(Tx4)
        for b in [B2, load_B1]:
            assert not b.is_valid()
