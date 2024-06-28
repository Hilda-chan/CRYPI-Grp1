import Pyfhel
import face_recognition
import numpy as np
import cv2

def readImg(path):
    img = cv2.imread(path)
    return img
    #return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[:,:,::-1]

def getFaceVectors(img):
    # array of float (vectors)
    return face_recognition.face_encodings(img)[0]

def generateKeys():
    # (public_key, private_key)
    pbk, prk = paillier.generate_paillier_keypair()
    return (pbk, prk)

def compare(v1, v2):
    tmp = v1 - v2
    return np.sum(np.square(tmp))
    #return np.mean(tmp)

def encryptVector(pbk, v):
    res = np.array([])
    for i in range(len(v)):
        res = np.append(res, pbk.encrypt(v[i]))#pbk.encrypt(v[i]))
    return res

def decrypt(prk, res):
    return prk.decrypt(res)

def calculate(pbk, v1, v2):
    enc1 = encryptVector(pbk, v1)
    enc2 = encryptVector(pbk, v2)

    return compare(enc1, enc2)

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

path1 = "./LFW/Aaron_Pena_0001.jpg"
path2 = "./LFW/Aaron_Eckhart_0001.jpg"
path3 = "./LFW/Abel_Pacheco_0002.jpg"
path4 = "./LFW/Abel_Pacheco_0003.jpg"

img1 = readImg(path3)
img2 = readImg(path1)

HE = Pyfhel.Pyfhel()
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext.
                        #  Typ. 2^D for D in [10, 15]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': [60, 30, 30, 30, 60] # Number of bits of each prime in the chain.
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}
HE.contextGen(**ckks_params)  # Generate context for ckks scheme
HE.keyGen()

v1 = getFaceVectors(img1)
#test1 = HE.encrypt(v1)
v2 = getFaceVectors(img2)
#test2 = HE.encrypt(v2)

#enc = compare(test1, test2)
enc = calculate(HE, v1, v2)
print("Ecart moyen des vecteurs :")
result(np.mean(np.sqrt(HE.decrypt(enc))))
