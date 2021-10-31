import cv2
import face_recognition
import numpy as np
import time,os


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, img = self.video.read()
        face_cascade = cv2.CascadeClassifier('cascade_face_detect.xml')


        frame_width = int(self.video.get(3))
        frame_height = int(self.video.get(4))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 2, 1)
        print(faces)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            if x>180 and y>150 and w>180 and h>180:
                cv2.imwrite("test.png", img)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # print("-->>",img,img1)
        ret, img = cv2.imencode('.jpg', img)
        return img.tobytes()


class LoginCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        file1 = open("userdetails.txt","r")
        rd=file1.readlines()
        rd=rd[0].split("_")
        st="faces/"+rd[0]+".png"
        file1.close()
        my_img1 = face_recognition.load_image_file(st)
        my_img1_encos=face_recognition.face_encodings(my_img1)[0]
        known_face_enco = [
        my_img1_encos 
        ]
        known_face_names=[
        rd[1]
        ]
        face_cascade = cv2.CascadeClassifier('cascade_face_detect.xml')

        

        frame_width = int(self.video.get(3))
        frame_height = int(self.video.get(4))

        if (type(frame).__name__ != "NoneType"):
            rgb_frame = frame[:,:,::-1]
            face_locations=face_recognition.face_locations(rgb_frame)
            face_encos=face_recognition.face_encodings(rgb_frame,face_locations)
            name="Unknown"
            try:
                for (top,right,bottom,left), face_enco in zip(face_locations,face_encos):
                    matches=face_recognition.compare_faces(known_face_enco,face_enco)
                    name="Unknown"

                    if True in matches:
                        first_match_index=matches.index(True)
                        name=known_face_names[first_match_index]
                        ile1 = open("logged.txt","w")
                        ile1.write("Logged")
                        ile1.close()
                    cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
                    font=cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(255,255,255),1)
                if name=="Unknown":
                    print("Not found")
                else:
                    print("Found")
            except Exception as e:
                return e
        ret, img = cv2.imencode('.jpg', frame)
        return img.tobytes()