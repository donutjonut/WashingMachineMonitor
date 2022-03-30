import cv2 
import pytesseract 
import time 
from pushover import init, Client 
import requests

pushoverAPI = "" #pushover api key
clientID = "" #pushover client ID
particleCall = "" #particle argon integration link
frame_rate = 10 #preview frame rate (fps)


def main():
    #init pushover 
    init(pushoverAPI)
    #init cv2 
    cap = cv2.VideoCapture(0) 
    prev = 0 
    fps = cap.get(cv2.CAP_PROP_FPS) 
    print("CAMERA FPS: " + str(fps))

    while True:
        time_elapsed = time.time() - prev 
        res, image = cap.read() 
        #weird fps limit thing 
        if time_elapsed > 1./frame_rate:
            prev = time.time() 
            cv2.imshow("Frame", image) 
            text = pytesseract.image_to_string(image).lower() 
            print("INPUT: " + text) 
            pText = text[text.find("end") : text.find("end") + 3] 
            print("OUTPUT: " + pText) 
            if (pText == "end"):
                #notification 
                Client(clientID).send_message("Your laundry is done!", title="Washing Machine Monitor") 
                #particle 
                requests.post(particleCall) 
                #wait
                break 
            if cv2.waitkey (1) & 0xFF == ord ("s"):
                print("stopped")
                break 
    cv2.destroyAllWindows()
if __name__== "__main__":
    main()