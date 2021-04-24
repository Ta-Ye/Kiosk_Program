# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np


class FaceRecog():

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        dirname = '../image/member'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                fff=face_recognition.face_encodings(img)
                if fff:
                    face_encoding = fff[0]
                    self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def __del__(self):
        del self.camera

    def get_frame(self):

        global save
        save = []

        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #small_frame = frame

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                #print(distances)
                #print(len(distances))

                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                distances=[(idx,i) for idx, i in enumerate(distances)]
                distances.sort(key=lambda x: x[1])
                for i in range(0, len(distances)):                    
                    if distances[i][1] < 0.45:
                        #print(face_recog.known_face_names[distances[i][0]])
                        save.append(face_recog.known_face_names[distances[i][0]])
                        #index = np.argmin(distances)
                        #name = self.known_face_names[index]
                    else:
                        break

                #print(" ")
                #print(save)

                #self.face_names.append(name)

        
        self.process_this_frame = not self.process_this_frame

        return save
        
    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


face_recog = FaceRecog()
def your_face():
    check=0
    while check == 0:
        save1 = face_recog.get_frame()
        if not save1:
            pass
        else:
            check = 1
    return save1
