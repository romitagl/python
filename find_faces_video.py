import sys
import cv2
import time

# This line sets the video source to the default webcam (VideoCapture(0) always points to the default webcam) if no video file is specified. Else, it loads the file.
if len(sys.argv) < 2:
    video_capture = cv2.VideoCapture(0)
else:
    video_capture = cv2.VideoCapture(sys.argv[1])

# load the OpeCV default cascade for detecting faces 
cascPath = './cascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascPath)

while True:
  # Capture frame-by-frame
  ret, image = video_capture.read()

  if not ret:
    break

  scale_percent = 50 # percent of original size
  height = int(image.shape[0] * scale_percent / 100)
  width = int(image.shape[1] * scale_percent / 100)
  new_dim = (width, height)
  # resize image
  image_resized = cv2.resize(image, new_dim, interpolation = cv2.INTER_AREA)

  #convert to grayscale
  gray_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
  
  faces = face_cascade.detectMultiScale(
    gray_image,
    scaleFactor = 1.2,
    minNeighbors = 5,
    minSize = (30,30)
    )

  # Draw a rectangle around the faces
  for (x, y, w, h) in faces:
      cv2.rectangle(image_resized, (x, y), (x+w, y+h), (0, 255, 0), 2)

  cv2.imshow("Faces found", image_resized)
  # delay each frame display
  cv2.waitKey(100)

video_capture.release()
cv2.destroyAllWindows()
