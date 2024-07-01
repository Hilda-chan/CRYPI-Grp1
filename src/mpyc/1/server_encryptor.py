from ctypes import *
import Pyfhel
import face_recognition
import numpy as np
import cv2
import os

def readImg(path):
    img = cv2.imread(path)
    return img

def getFaceVectors(img):
    return face_recognition.face_encodings(img)[0]

def generateKeys():
    pbk, prk = paillier.generate_paillier_keypair()
    return (pbk, prk)

def compare(v1, v2):
    tmp = v1 - v2
    return np.sum(np.square(tmp))

def encryptVector(pbk, v):
    res = np.array([])
    for i in range(len(v)):
        res = np.append(res, pointer(pbk.encrypt(v[i])))#pbk.encrypt(v[i]))
    return res

def decrypt(HE, res):
    return np.mean(np.sqrt(HE.decrypt(res)))

def calculate(pbk, v1):
    enc1 = encryptVector(pbk, v1)
    return enc1

def result(dst):
    seuil = 0.6
    print("Distance Euclidienne entre les deux visages :")
    print(dst)
    if dst < seuil :
        print("La personne est authentifié.")
        return True
    else :
        print("La personne n'est pas reconnue.")
        return False

def serv_encrypt(username):
    path = "data/LFW/" + username + "/" + username +"_0001.jpg"

    img = readImg(path)
    vectors = getFaceVectors(img)
    
    return (vectors)