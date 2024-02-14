import transactions
import txblock
import signatures
import client

class TestClient:

    def test_send_block():
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

        client.sendBlock('localhost', B1)

        client.sendBlock('localhost', Tx2)
