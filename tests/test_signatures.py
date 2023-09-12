import signatures

class TestSignatures:

    def test_verify(self):
        pr,pu = signatures.generate_keys()
        message = "This is a secret message"
        sig = signatures.sign(message, pr)
        assert signatures.verify(message, sig, pu)
        
    def test_attack(self):
        pr,pu = signatures.generate_keys()
        message = "This is a secret message"
        
        # Generate an attacker's public and private keys
        pr2, pu2 = signatures.generate_keys()

        # Try to sign with the attacker's private key and pass it off as
        # another user's signature
        sig_attacker = signatures.sign(message, pr2)

        assert not signatures.verify(message, sig_attacker, pu)

    def test_modification(self):
        pr,pu = signatures.generate_keys()
        message = "This is a secret message"
        sig = signatures.sign(message, pr)
        # Modify the message and try to pass the original signature
        badmess = message + "Q"
        assert not signatures.verify(badmess, sig, pu)
