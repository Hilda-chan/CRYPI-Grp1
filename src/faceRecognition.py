import dlib
import cv2
import numpy as np


image_path = 'data/LFW/Aaron_Eckhart/Aaron_Eckhart_0001.jpg'
image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = gray.astype(np.uint8)

detector = dlib.get_frontal_face_detector()

faces = detector(gray)

for face in faces:
    x, y, w, h = (face.left(), face.top(), face.width(), face.height())
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('Detected Faces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()