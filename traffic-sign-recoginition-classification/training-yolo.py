from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("./weights/best.pt")
    model.predict(source=0, show=True)
