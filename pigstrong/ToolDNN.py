'''

@Author : Qiang Zhu , Xixiang Lv
@Time : 2018/10/01
@license : Copyright(C), Qiang Zhu , Xixiang Lv. All rights reserved.
@Contact : qzhu@stu.xidian.edu.cn
@Reference Paper : "2P-DNN : Privacy-Preserving Deep Neural Networks Based on Homomorphic Cryptosystem"

In this file, we offer you some functions for 2P-DNN model.

'''
import phe

def linearTrans(inputVec,w,b,public_key):
    E0 = public_key.encrypt(0)
    n = len(w)
    m = len(w[0])
    outputVec = []
    for i in range(n):
        tempVec = E0
        for j in range(m):
            tempX = phe.paillier.EncryptedNumber.__mul__(inputVec[j],w[i][j])
            tempVec = phe.paillier.EncryptedNumber._add_encrypted(tempVec,tempX)
            print(i,j)
        tempVec = phe.paillier.EncryptedNumber._add_encrypted(tempVec, b[i])
        outputVec.append(tempVec)
    return outputVec


def CryptoReLU(inputVec,public_key, private_key):
    E0 = public_key.encrypt(0)
    n = len(inputVec)
    for i in range(n):
        temp = private_key.decrypt(inputVec[i])
        if(temp<0):
            inputVec[i] = E0
            print(i)
    return inputVec


def AveragePooling(inputTensor,public_key, private_key):  #poolingKernel  SAME

    E0 = public_key.encrypt(0)
    n = len(inputTensor)
    if(n%2 == 1):
        for i in range(n):
            inputTensor[i].append(E0)
        tempVec0 = [0 for i in range(n+1)]
        inputTensor.append(tempVec0)
    n = len(inputTensor)
    outputTensor = []
    for i in range(0,n,2):
        tempOut = []
        for j in range(0,n,2):
            tempV = phe.paillier.EncryptedNumber.__add__(inputTensor[i][j],inputTensor[i][j+1])
            tempV = phe.paillier.EncryptedNumber.__add__(tempV, inputTensor[i+1][j])
            tempV = phe.paillier.EncryptedNumber.__add__(tempV, inputTensor[i+1][j+1])
            tempOut.append(tempV)
            print(i,j)
        outputTensor.append(tempOut)

    return outputTensor

def cov2d(inputTensor,covKernel,public_key, private_key,Ebias):    #covKernel  SAME
    n = len(inputTensor)
    E0 = public_key.encrypt(0)
    tensor = [[E0 for i in range(n+2)] for j in range(n+2)]
    for i in range(n):
        for j in range(n):
            tensor[i+1][j+1] = inputTensor[i][j]
    outputTensor = []
    for i in range(n):
        tempOut = []
        for j in range(n):
            tempV = E0
            for z in range(3):
                for w in range(3):
                    t = phe.paillier.EncryptedNumber.__mul__(tensor[i+z][j+w],round(covKernel[z][w]*10000))
                    print(type(tempV),type(t))
                    tempV = phe.paillier.EncryptedNumber._add_encrypted(tempV, t)
                    print(i,j,z,w)
            tempV = phe.paillier.EncryptedNumber._add_encrypted(tempV, Ebias)
            tempOut.append(tempV)
        outputTensor.append(tempOut)

    return outputTensor
