from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad


mat_str = open('MAT_STR.txt').read()
KEY_LENGTH = 128

key = SHA256.new(data=mat_str.encode()).digest()[:KEY_LENGTH]
flag = {"iv": "43f14157442d75142d0d4993e99a9582", "ciphertext": "22abc3b347ffef55ec82488e5b4a338da5af7ef1918ac46f95029a4d94ace4cb2700fa9aeb31e6a4facee2601e99dabd6f9a81494c55f011e9227c9a6ae8d802"}
cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(flag['iv']))

pt = cipher.decrypt(bytes.fromhex(flag['ciphertext']))

print(pt)
