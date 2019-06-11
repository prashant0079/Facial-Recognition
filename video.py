"""import numpy as np
import cv2
from urllib.request import urlopen

#cap = cv2.VideoCapture('rtsp://192.168.42.1/live',cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print(cap.isOpened())
url = "http://192.168.42.1/live"
imgResp = urlopen(url)
byteImg = np.array(bytearray(imgResp.read()), dtype=np.uint8)
img = cv2.imdecode(byteImg, -1)
print(img)
cv2.imshow('video', img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
import cv2
import numpy as np
import vlc
import time

player=vlc.MediaPlayer('rtsp://192.168.42.1/live')
player.play()
time.sleep(5)

while 1:
    time.sleep(0.01)
    player.video_take_snapshot(0, '.tmp.png', 0, 0)
    frame = cv2.imread('.tmp.png')
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
    	break

cv2.destroyAllWindows()    	



