'''
https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#cryptography.hazmat.primitives.hashes.Hash
'''
from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())
digest.update(b"abc")
digest.update(b"123")
print(digest.finalize())

digest = hashes.Hash(hashes.SHA256())
digest.update(b"abc")
digest.update(b"124")
print(digest.finalize())
