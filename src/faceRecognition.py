import dlib
import cv2
import matplotlib.pyplot as plt


image_path = 'data/LFW/Aaron_Eckhart/Aaron_Eckhart_0001.jpg'
image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


detector = dlib.get_frontal_face_detector()

faces = detector(gray)

for face in faces:
    x, y, w, h = (face.left(), face.top(), face.width(), face.height())
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()