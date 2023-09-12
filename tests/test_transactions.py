from transactions import Tx
import signatures

class TestTransactions:
    
    def test_is_valid(self):
        pr1, pu1 = signatures.generate_keys()
        pr2, pu2 = signatures.generate_keys()
        pr3, pu3 = signatures.generate_keys()
        pr4, pu4 = signatures.generate_keys()

        Tx1 = Tx()
        Tx1.add_input(pu1, 1)
        Tx1.add_output(pu2, 1)
        Tx1.sign(pr1)
        assert Tx1.is_valid()

        Tx2 = Tx()
        Tx2.add_input(pu1, 2)
        Tx2.add_output(pu2, 1)
        Tx2.add_output(pu3, 1)
        Tx2.sign(pr1)

        Tx3 = Tx()
        Tx3.add_input(pu3, 1.2)
        Tx3.add_output(pu1, 1.1)
        Tx3.add_required(pu4)
        Tx3.sign(pr3)
        Tx3.sign(pr4)

        for t in [Tx1, Tx2, Tx3]:
            assert t.is_valid()

        # Wrong signatures
        Tx4 = Tx()
        Tx4.add_input(pu1, 1)
        Tx4.add_output(pu2, 1)
        Tx4.sign(pr2)

        # Escrow Tx not signed by the arbiter
        Tx5 = Tx()
        Tx5.add_input(pu3, 1.2)
        Tx5.add_output(pu1, 1.1)
        Tx5.add_required(pu4)
        Tx5.sign(pr3)

        # Two input addrs, signed by one
        Tx6 = Tx()
        Tx6.add_input(pu3, 1)
        Tx6.add_input(pu4, 0.1)
        Tx6.add_output(pu1, 1.1)
        Tx6.sign(pr3)

        # Outputs exceed inputs
        Tx7 = Tx()
        Tx7.add_input(pu4, 1.2)
        Tx7.add_output(pu1, 1)
        Tx7.add_output(pu2, 2)
        Tx7.sign(pr4)

        # Negative values
        Tx8 = Tx()
        Tx8.add_input(pu2, -1)
        Tx8.add_output(pu1, -1)
        Tx8.sign(pr2)

        # Negative values on output only
        Tx81 = Tx()
        Tx81.add_input(pu2, 1)
        Tx81.add_output(pu1, -1)
        Tx81.sign(pr2)

        # Modified Tx
        Tx9 = Tx()
        Tx9.add_input(pu1, 1)
        Tx9.add_output(pu2, 1)
        Tx9.sign(pr1)
        # outputs = [(pu2,1)]
        # change to [(pu3,1)]
        Tx9.outputs[0] = (pu3,1)
        
        # all invalid transactions for one reason or another
        for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx81, Tx9]:
            assert not t.is_valid()
    