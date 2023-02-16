import cv2
import os
import os
import numpy as np
from PIL import Image
import cv2
import pickle


faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

# Specify the `user_name` and `NUM_IMGS` here.
def capture_and_train(user_name):
    user_name = user_name
    NUM_IMGS = 500
    if not os.path.exists('data/{}'.format(user_name)):
        os.mkdir("data/{}".format(user_name))

    cnt = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (350, 50)
    fontScale = 1
    fontColor = (102, 102, 225)
    lineType = 2

    # Open camera
    while cnt <= NUM_IMGS:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        msg = "Saving {}'s Face Data [{}/{}]".format(user_name, cnt, NUM_IMGS)
        cv2.putText(frame, msg,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        # Store the captured images in `data/Jack`
        cv2.imwrite("data/{}/{}{:03d}.jpg".format(user_name, user_name, cnt), frame)
        cnt += 1
        print(msg)

        key = cv2.waitKey(100)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "data")

    # Load the OpenCV face recognition detector Haar
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    # Create OpenCV LBPH recognizer for training
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_label = []
    x_train = []

    # Traverse all face images in `data` folder
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace("", "").upper()  # name
                print(label, path)

                if label in label_ids:
                    pass
                else:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L")
                image_array = np.array(pil_image, "uint8")
                print(image_array)
                # Using multiscle detection
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_label.append(id_)

    # labels.pickle store the dict of labels.
    # {name: id}  
    # id starts from 0
    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)

    # Train the recognizer and save the trained model.
    recognizer.train(x_train, np.array(y_label))
    recognizer.save("train.yml")

capture_and_train("Derek")
