import dlib
import cv2
import numpy as np
import face_recognition


detector = dlib.get_frontal_face_detector()



def GetFacesFromPicture(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.uint8)
    faces = detector(gray)

    face_regions = []
    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        face_region = input_image[y:y+h, x:x+w]
        face_regions.append(face_region)

    return face_regions


def getFaceVectors(img):
    # array of float (vectors)
    return face_recognition.face_encodings(img)[0]


def ShowFaces(faces):
    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(input, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detected Faces', input)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

