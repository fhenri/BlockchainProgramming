import server

class TestServer:
    
    def test_recvObj(self):
        s = server.new_connection('192.168.0.27')
        newB = s.receive_object(s)
        print (newB.data[0])
        print (newB.data[1])
        assert newB.is_valid(), "ERROR. Tx is invalid"
        assert newB.data[0].inputs[0][1] == 2.3, "Error! Wrong input value for block 1, tx 1"
        assert newB.data[0].outputs[1][1] == 1.1, "Error! Wrong output value for block 1, tx 1"
        assert newB.data[1].inputs[0][1] == 2.3, "Error! Wrong input value for block 1, tx 1"
        assert newB.data[1].inputs[1][1] == 1.0, "Error! Wrong input value for block 1, tx 1"
        assert newB.data[1].outputs[0][1] == 3.1, "Error! Wrong output value for block 1, tx 1"
        
        newTx= s.receive_object(s)
        print (newTx)
