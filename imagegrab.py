import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
 
while(True):
    last_time = time.time()
    # 800x600 windowed mode
    printscreen =  np.array(ImageGrab.grab(bbox=(50,50,400,400)))
    print('loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

