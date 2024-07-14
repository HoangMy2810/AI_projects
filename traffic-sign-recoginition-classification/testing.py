import numpy as np
import cv2 as cv
from keras import models
from skimage import transform, exposure
from ultralytics import YOLO
from time import time
from PIL import Image
from customtkinter import CTkImage


def image_processing(image):
    image = transform.resize(image, (32, 32))
    image = exposure.equalize_adapthist(image,
                                        clip_limit=0.1)
    image = image.astype("float32") / 255.0
    return image


def getClassName(classNo):
    classes = ['Speed limit (20km/h)',
               'Speed limit (30km/h)',
               'Speed limit (50km/h)',
               'Speed limit (60km/h)',
               'Speed limit (70km/h)',
               'Speed limit (80km/h)',
               'End of speed limit (80km/h)',
               'Speed limit (100km/h)',
               'Speed limit (120km/h)',
               'No Overtaking',
               'No Overtaking for Heavy Vehicles',
               'Right-of-Way at next Intersection',
               'Priority Road',
               'Yield',
               'Stop',
               'No Vehicles',
               'Heavy Vehicles Prohibited',
               'No Entry',
               'General Caution',
               'Dangerous Left Curve',
               'Dangerous Right Curve',
               'Double Curve',
               'Bumpy Road',
               'Slippery Road',
               'Narrowing Road',
               'Road Work',
               'Traffic Signals',
               'Pedestrian',
               'Children',
               'Bike',
               'Snow',
               'Deer',
               'End of Limits',
               'Turn Right Ahead',
               'Turn Left Ahead',
               'Ahead Only',
               'Go Straight or Right',
               'Go Straight or Left',
               'Keep Right',
               'Keep Left',
               'Roundabout Mandatory',
               'End of No Overtaking',
               'End of No Overtaking for Heavy Vehicles']
    return classes[classNo]


def predictImage(image, model):
    image = image_processing(image)
    image = image.reshape(1, 32, 32, 3)
    prediction = model.predict(image, verbose=0)
    return prediction


def start_webcam_inference(model_name, use_video, camgui=None):
    frameWidth = 640
    frameHeight = 640
    brightness = 180
    threshold = 0.5
    font = cv.FONT_HERSHEY_SIMPLEX

    if use_video:
        print("\nLoading Video...")
        cap = cv.VideoCapture(r"video.mp4")
    else:
        print("\nLoading webcam...")
        cap = cv.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)

    # IMPORT THE TRAINED MODEL
    print("\nLoading trained models...")
    t1 = time()
    yolo_model = YOLO("./weights/best.pt")
    print(f"Loaded YOLO model...")
    t1 = time()
    model = models.load_model('./Models/' + model_name)
    print(f"Loaded CNN model...")

    print("\nBeginning...")
    while True:
        success, imgOriginal = cap.read()
        img = np.asarray(imgOriginal)

        results = yolo_model.predict(source=img, verbose=True)
        img_plotted = results[0].plot()
        x1, y1, x2, y2 = 0, 0, 0, 0
        detected = False
        try:
            boxes = results[0].boxes
            box = boxes[0]
            x1 = int(box.xyxy[0][0])
            y1 = int(box.xyxy[0][1])
            x2 = int(box.xyxy[0][2])
            y2 = int(box.xyxy[0][3])
            detected = True
        except Exception:
            pass

        if detected:
            roi = img[y1:y2, x1:x2]

            predictions = predictImage(roi, model)
            classIndex = np.argmax(predictions)
            probabilityValue = np.amax(predictions)

            if probabilityValue > threshold:
                cv.putText(img_plotted, "CLASS: " + str(classIndex) + " " + str(getClassName(classIndex)), (8, 24),
                           font, 0.50, (0, 0, 255), 1, cv.LINE_AA)
                cv.putText(img_plotted, "PROBABILITY: " + str(round(probabilityValue * 100, 2)) + "%", (8, 48),
                           font, 0.50, (0, 0, 255), 1, cv.LINE_AA)
                print(f"Detected Traffic Sign.\tClass: {classIndex}\t"
                      f"Probability: {round(probabilityValue * 100, 2):02.2f}%\t\t"
                      f"Name: {getClassName(classIndex)}")

        if camgui is None:
            cv.imshow("e", img_plotted)
        else:
            cvimage = cv.cvtColor(img_plotted, cv.COLOR_BGR2RGBA)
            image = Image.fromarray(cvimage)
            imgctk = CTkImage(image, size=(640, 480))
            camgui.image_label.configure(image=imgctk)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    print("Closing Inference Window...")
