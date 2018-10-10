'''

@Author : Qiang Zhu , Xixiang Lv
@Time : 2018/10/01
@license : Copyright(C), Qiang Zhu , Xixiang Lv. All rights reserved.
@Contact : qzhu@stu.xidian.edu.cn
@Reference Paper : "2P-DNN : Privacy-Preserving Deep Neural Networks Based on Homomorphic Cryptosystem"

This file is a demo of 2P-DNN model. You can change the input_Path for your own MNIST input picture. We also
offer you some MNIST input picture in "input_Image". You can use them derictly. The paillier is very very
slow, so you need some patience.

'''

import phe
from skimage import io
import datetime
import ToolDNN
import numpy as np
import ImageCrypto
starttime = datetime.datetime.now()

print('------------------paillier key start-------------------')
public_key, private_key = phe.paillier.generate_paillier_keypair()
print('------------------image crypto successful-------------------')

print('------------------image crypto start-------------------')
input_Path = './parameter/90.jpg'
img=io.imread(input_Path )
inputImg = img.tolist()
n = len(inputImg)
for i in range(n):
    for j in range(n):
        inputImg[i][j] = public_key.encrypt(inputImg[i][j])
print('------------------image crypto successful-------------------')

print('------------------load parameter start-------------------')
# wconv1 = np.load('./parameter/wconv1.npy')
# bconv1 = np.load('./parameter/bconv1.npy').tolist()
# wconv2 = np.load('./parameter/wconv2.npy')
# bconv2 = np.load('./parameter/bconv2.npy').tolist()
# wfc1 = np.load('./parameter/wfc1.npy').tolist()
# bfc1 = np.load('./parameter/bfc1.npy').tolist()
# wfc2 = np.load('./parameter/wfc2.npy').tolist()
# bfc2 = np.load('./parameter/bfc2.npy').tolist()
w1 = np.load('./parameter/w1.npy')
b1 = np.load('./parameter/b1.npy').tolist()
w2 = np.load('./parameter/w2.npy')
b2 = np.load('./parameter/b2.npy').tolist()
print('------------------load parameter successful-------------------')


print('------------------bias crypto start-------------------')
# Ebconv1 = []
# for i in bconv1:
#     Ebconv1.append(public_key.encrypt(i))
# Ebconv2 = []
# for i in bconv2:
#     Ebconv2.append(public_key.encrypt(i))
# Ebfc1 = []
# for i in bfc1:
#     Ebfc1.append(public_key.encrypt(i))
# Ebfc2 = []
# for i in bfc2:
#     Ebfc2.append(public_key.encrypt(i))
Eb1 = []
for i in b1:
    Eb1.append(public_key.encrypt(i))
Eb2 = []
for i in b2:
    Eb2.append(public_key.encrypt(i))
print('------------------bias crypto successful-------------------')


print('------------------reshape parameter start-------------------')
# wconv1 = wconv1.reshape((3,3,32))
# wconv1 = np.transpose(wconv1,(2,0,1))
# wconv1= wconv1.tolist()
w1 = np.transpose(w1,(1,0)).tolist()
w2 = np.transpose(w2,(1,0)).tolist()


print('------------------reshape parameter successful-------------------')

#
# conv1Tensor = ToolDNN.cov2d(inputImg,wconv1[0],public_key, private_key,Ebconv1[0])
#
# ToolDNN.AveragePooling(conv1Tensor,public_key, private_key)

inputX = []
for i in inputImg:
    for j in i:
        inputX.append(j)
print(inputX)
print(len(inputX))

f1 = ToolDNN.linearTrans(inputX,w1,Eb1,public_key)
r1 = ToolDNN.CryptoReLU(f1,public_key, private_key)
f2 = ToolDNN.linearTrans(r1,w2,Eb2,public_key)
r2 = ToolDNN.CryptoReLU(f2,public_key, private_key)
outArr = []
for i in r2:
    outArr.append(private_key.decrypt(i))
print(outArr)

outID = 0
tempMax = outArr[0]
for i in range(10):
    if(outArr[i]>tempMax):
        outID = i
        tempMax = outArr[i]
print("predicted results:",outID)


endtime = datetime.datetime.now()

print("total time:",(endtime - starttime).seconds,"seconds")
