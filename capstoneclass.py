import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller
import math
#from pynput.mouse import Button,Controller
import pyautogui


keyboard = Controller()
state = None
cap = cv2.VideoCapture(0)
hand = mp.solutions.hands
drawing = mp.solutions.drawing_utils

hands_object = hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5,max_num_hands=1)
width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
hieght=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width,hieght)

screen_width,screen_hieght=pyautogui.size()
print(screen_width,screen_hieght)

def count_fingers(lst,image):
    count=0
    global state

    threshholdData=(lst.landmark[0].y*100-lst.landmark[9].y*100)/2
    #print(threshholdData)
    
    if (lst.landmark[5].y*100-lst.landmark[8].y*100)>threshholdData:
        count+=1
    if (lst.landmark[9].y*100-lst.landmark[12].y*100)>threshholdData:
        count+=1
    if (lst.landmark[13].y*100-lst.landmark[16].y*100)>threshholdData:
        count+=1
    if (lst.landmark[17].y*100-lst.landmark[20].y*100)>threshholdData:
        count+=1
    # if (lst.landmark[5].x*100-lst.landmark[4].x*100)>6:
    #     count+=1
    total_finger_count=count

    if total_finger_count==4:
        state="play"
    if total_finger_count==0 and state=="play":
        state="pause"
        keyboard.press(Key.space)
        
    tipFinger_x=(lst.landmark[8].x)*width
    if total_finger_count==1:
        if tipFinger_x<width-100:
            state="backward"
            print("play backward")
            keyboard.press(Key.left)
        if tipFinger_x>width-100:
            state="forward"
            print("play forward")
            keyboard.press(Key.right)

    tipFinger_y=(lst.landmark[8].y)*hieght
    if total_finger_count==2:
        if tipFinger_y<hieght-200:
            state="volume increase"
            print("increase volume")
            pyautogui.press("volumeup")
        if tipFinger_y>hieght-200:
            state="volume decrease"
            print("decrease volume")
            pyautogui.press("volumedown")

    return total_finger_count


    
while True:
    success, image = cap.read()
    image=cv2.flip(image,1)

    
    # Detect the Hands Landmarks 
    results = hands_object.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    #print(results)

    if results.multi_hand_landmarks:
         hand_keyPoints=results.multi_hand_landmarks[0]
         #print(hand_keyPoints) 
         c=count_fingers(hand_keyPoints,image)
         cv2.putText(image,"fingers: "+str(c),(50,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
         cv2.putText(image,"state: "+str(state),(200,100),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
         drawing.draw_landmarks(image,hand_keyPoints,hand.HAND_CONNECTIONS)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()