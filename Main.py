
import cv2
import numpy as np
import HandTracking as ht
import pyautogui
import autopy
pyautogui.FAILSAFE = False
### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 5         # Smoothening Factor
sens = 0.4        # sensitivity
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size
mf_ = if_ = mfb_ = mf_old = if_old = mfb_old =  (0,0)
movement=l_click=r_click=0
while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, c = img.shape
    
    if len(lmlist)!=0:
        x1, y1 = lmlist[6][1:]
        x2, y2 = lmlist[10][1:]
        
        x1 = (x1+x2)/2
        y1 = (y1+y2)/2
        

        fingers = detector.fingersUp()      # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0: #and fingers[0] == 0:
            fm_d = detector.findDistance(8, 12, img)[0]
            if fm_d <= 40:
                if movement==1:
                    curr_x = x1
                    curr_y = y1
                    
                    x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
                    y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))
                    curr_x = prev_x + (x3 - prev_x)/smoothening
                    curr_y = prev_y + (y3 - prev_y) / smoothening
                    autopy.mouse.move(screen_width - curr_x, curr_y)    # Moving the cursor
                    #pyautogui.moveTo(screen_width - curr_x, curr_y)    # Moving the cursor
                    
                else:
                    movement = 1
            prev_x, prev_y = curr_x, curr_y
            l_click=r_click=0

        elif l_click == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:     # If fore finger & middle finger both are up
            
        
            pyautogui.click(button='left')
            l_click = 1
            movement = 0
            
        elif r_click == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:     # If fore finger & middle finger both are up
           
            pyautogui.click(button='right')
            r_click = 1
            movement = 0
            
        elif fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1: 
            tf_d = detector.findDistance(4, 8, img)[0]
            if tf_d < 40:
                curr_x,curr_y = x1,y1
                if prev_y != 0 and curr_y < prev_y:
                    pyautogui.press('volumeup')
                elif prev_y != 0 and curr_y > prev_y:
                    pyautogui.press('volumedown')
                prev_x, prev_y = curr_x, curr_y
                movement = 0
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1: 
            tf_d = detector.findDistance(4, 20, img)[0]
            if tf_d < 40:
                curr_x,curr_y = x1,y1
                if prev_y != 0 and curr_y < prev_y:
                    pyautogui.scroll(100)
                elif prev_y != 0 and curr_y > prev_y:
                    pyautogui.scroll(-100)
                prev_x, prev_y = curr_x, curr_y
                movement = 0
    
    cv2.imshow("Output",cv2.flip(img,1))
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    cv2.waitKey(1)

cv2.destroyAllWindows()
cap.release()    