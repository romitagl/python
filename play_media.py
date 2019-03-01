import sys
import cv2
import imghdr
import time

# media viewer - handles image or video types
# press any botton to quit image viewer

def play_media(argv):
  if len(argv) != 2:
    print('Specify the media file path as input parameter! e.g.: play_media.py ./media.jpg')
    sys.exit(2)
  else:
    if(imghdr.what(argv[1]) != None): # picture file
      print('Press any botton to quit...\n')
      media_capture = cv2.imread(argv[1])
      cv2.imshow("Image viewer", media_capture)
      cv2.waitKey(0)
    else: # video file
      media_capture = cv2.VideoCapture(argv[1])
      # get the frames per second of the input video
      fps = media_capture.get(cv2.CAP_PROP_FPS)
      print('Playing video at: %d fps', fps)

      while True:
        # Capture frame-by-frame
        ret, image = media_capture.read()

        if not ret:
          sys.exit(2)

        cv2.imshow("Media player", image)
        # delay each frame display
        k = cv2.waitKey(int(1000/fps)) & 0xFF
        if k == 27: # ESC
          sys.exit(0)

      media_capture.release()
  cv2.destroyAllWindows()
  
if __name__ == "__main__":
   play_media(sys.argv)
