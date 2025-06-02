import face_recognition
import cv2
import json

path = "attendeeImages"
curImage = cv2.imread(f'../{path}/james_maddison.jpg')
name = "james maddison"

curImage = cv2.cvtColor(curImage, cv2.COLOR_BGR2RGB)
imgEncoding = face_recognition.face_encodings(curImage)[0]

# Below is an example of a numpy array
# encoding = np.random.rand(128).astype(np.float64)
imgEncoding = list(imgEncoding)
jsonEncoding = json.dumps(imgEncoding)   # encode into json


print(imgEncoding)
print(jsonEncoding)

print("Encoding Complete!")