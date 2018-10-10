'''

@Author : Qiang Zhu , Xixiang Lv
@Time : 2018/10/01
@license : Copyright(C), Qiang Zhu , Xixiang Lv. All rights reserved.
@Contact : qzhu@stu.xidian.edu.cn
@Reference Paper : "2P-DNN : Privacy-Preserving Deep Neural Networks Based on Homomorphic Cryptosystem"

'''
from skimage import io

def imageCrypto(inputPath,public_key):

    img=io.imread(inputPath)
    inputImg = img.tolist()
    n = len(inputImg)
    for i in range(n):
        for j in range(n):
            inputImg[i][j] = public_key.encrypt(inputImg[i][j])
    return inputImg