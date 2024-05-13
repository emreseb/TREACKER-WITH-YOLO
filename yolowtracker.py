from ultralytics import YOLO
import cv2
import math 

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)


model = YOLO("best11.pt")


classNames = ["Person", "Person-Like"
              ]

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    
    for r in results:
        boxes = r.boxes

        for box in boxes:
            
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 

            
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)


            
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

def getCoordinates(image_width, image_height, box):
    x_center, y_center, width, height = box.xyxy[0]
    x_center_pixel = x_center * image_width
    y_center_pixel = y_center * image_height
    halfwidth = width * image_width / 2
    halfheight = height * image_height / 2

    xmin = int(x_center_pixel - halfwidth)
    ymin = int(y_center_pixel - halfheight)
    xmax = int(x_center_pixel + halfwidth)
    ymax = int(y_center_pixel + halfwidth)
    return xmin, ymin, xmax, ymax
    

cap.release()
cv2.destroyAllWindows()