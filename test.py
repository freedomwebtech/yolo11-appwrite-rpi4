import cv2
import pandas as pd
from ultralytics import YOLO
from paddleocr import PaddleOCR
from tracker import Tracker
import cvzone
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from datetime import datetime

ocr = PaddleOCR()

client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
client.set_project('678df87a00219b30c15f') # Your project ID
client.set_key('standard_875cfa0696fedf2880fb45665b6d580a83612889ce7e002c43d93878f166c36a631a3578cc9dfd989a1020dd60eb0bcb1062dc96fe01c4b77bf2695d756222b9adddbc1a1638b3f88ee34100585d1ae221976647dc47636fabab3ddeac5d50a57663bb7efcf4193ccb4e06ef688d3c5f60db879e4fae65f5848f552883a22dfa') # The user session to authenticate with



databases = Databases(client)


model = YOLO('best_full_integer_quant_edgetpu.tflite')


cap = cv2.VideoCapture('num1.mp4')



frame_count = 0
cy1=79
offset=10
tracker=Tracker()
def perform_ocr(image_array):
    if image_array is None:
        raise ValueError("Image is None")
    
    # Perform OCR on the image array
    results = ocr.ocr(image_array, rec=True)  # rec=True enables text recognition
    detected_text = []

    # Process OCR results
    if results[0] is not None:
        for result in results[0]:
            text = result[1][0]
            detected_text.append(text)

    # Join all detected texts into a single string
    return ''.join(detected_text)

list1=[]

# Provide your database_id and collection_id
database_id = "NUMBERPLATE"  # Replace with your database ID
collection_id = "DATA"  # Replace with your collection ID
# Data to store
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame=cv2.resize(frame,(1020,600))
    

    frame_count += 1
    if frame_count % 2 != 0:
        continue

    results = model.predict(frame,imgsz=240)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list=[]
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
    
       
        list.append([x1,y1,x2,y2])
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        if cy1<(cy+offset) and cy1>(cy-offset):

           if list1.count(id)==0:
               list1.append(id)
               crop = frame[y3:y4, x3:x4]
               crop = cv2.resize(crop, (120, 85))
               text = perform_ocr(crop)
               print(f"Detected Number Plate: {text}")
               # Get current date and time
               current_date = datetime.now().strftime('%Y-%m-%d')
               current_time = datetime.now().strftime('%I:%M:%S %p')
               result = databases.create_document(
                        database_id=database_id,           # Pass the database ID
                        collection_id=collection_id,       # Pass the collection ID
                        document_id=ID.unique(),           # Use unique() to auto-generate a unique ID
                        data={
                             "NUMBERPLATE": text,     # Data to be inserted
                             "DATE": current_date,
                             "TIME": current_time,
    }
)


#           cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
#        cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

    cv2.line(frame,(1,79),(1019,79),(0,0,255),2)
    cv2.imshow("FRAME", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
