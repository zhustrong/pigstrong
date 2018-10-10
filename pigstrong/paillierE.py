import phe
import numpy as np
import datetime

starttime = datetime.datetime.now()

public_key, private_key = phe.paillier.generate_paillier_keypair()
print(public_key)
x = 2.45616
y = 2000
a = -2
z = 3
ex = public_key.encrypt(x)
ey = public_key.encrypt(y)
ez = public_key.encrypt(z)
# enx = phe.encoding.EncodedNumber(x)
# e = phe.paillier.EncryptedNumber.__mul__(ex,a)
# e = phe.paillier.EncryptedNumber.__add__(ex,a)
# e = phe.paillier.EncryptedNumber.__add__(e,ez)
# e = phe.paillier.EncryptedNumber.__mul__(e,a)
# e = phe.paillier.EncryptedNumber.__add__(e,0)
# e = phe.paillier.EncryptedNumber.__mul__(ey,round(x*100000))
e = phe.paillier.EncryptedNumber.__mul__(ey,round(56465.654654))


d = private_key.decrypt(e)
print(d)
# randArray = np.random.randint(0,255,size=(784))
# a = randArray.tolist()
# print(a)
#
# for i in range(len(a)):
#     a[i] = public_key.encrypt(a[i])
#
# print(a)
#
# endtime = datetime.datetime.now()
#
# print((endtime - starttime).seconds)

