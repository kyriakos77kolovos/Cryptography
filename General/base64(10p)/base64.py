from pybase64 import standard_b64encode
from binascii import unhexlify

hex_encoded_string = unhexlify("72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf")
encoded_b64 = standard_b64encode(hex_encoded_string)
print(encoded_b64.decode())