import face_recognition
import cv2

def readImg(path):
    img = cv2.imread(path)
    return img

def getFaceVectors(img):
    return face_recognition.face_encodings(img)[0]

def toUsername(firstname, lastname):
    firstname = firstname.capitalize().replace(" ", "")
    lastname = lastname.capitalize().replace(" ", "")

    return f"{firstname}_{lastname}"
    
def cli_encrypt(username, path):
    img = readImg(path)
    vectors = getFaceVectors(img) 
    return (vectors)
