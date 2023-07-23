from Crypto.Hash import SHA256
from Crypto.Util.number import *
from Crypto.Cipher import AES
    


#Basic explanation on how to get number
#Get Jordan normal form of generator (Matrices J and P such that G = P*J*P^-1) 
#Realize that J is **almost** diagonal except for last 2 which form a 2x2 Jordan Block
#Let this Jordan block be K = [[E, 1], [0, E]]
#K^n = [[E^n, n*E^(n-1)], [0, E^n]]
#Let A = P^-1*w
#Let B = P^-1 * v
#K^n * [B[-2], B[-1]] = [A[-2], A[-1]]
#A[-1] = B[-1]*E^n
#A[-2] = B[-2]*E^n + B[-1]*n*E^(n-1)
#A[-2] = A[-1]/B[-1]*B[-2] + A[-1]*n/E
#n = (A[-2] - A[-1]/B[-1]*B[-2])E/A[-1]

KEY_LENGTH = 128
KEY = SHA256.new(data=b'5959805911241109643914928800631944794321671043586961836890946136294554770507810148857251869110638484873235200204605081157845088692257708370810040562721345').digest()[:KEY_LENGTH]
iv = bytes.fromhex('334b1ceb2ce0d1bef2af9937cf82aad6')
cipher = AES.new(KEY, AES.MODE_CBC, iv)
ct = bytes.fromhex('543e29415bdb1f694a705b2532a5beb7ebd7009591503ef3c4fbcebf9e62fe91307e5d98efcd49f9f3b1985956cafc89')
ans = cipher.decrypt(ct)

print(ans)
