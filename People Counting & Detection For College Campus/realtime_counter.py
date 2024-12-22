import argparse
import imutils
import pickle
import cv2
import json
import sys
import signal
import os
import numpy as np
import traceback
import os
import cv2
import numpy as np
import face_recognition
from video_capture import VideoCapture
import imutils
import cv2
import dlib
import threading
import datetime
import sendEmail
import constant

# To properly pass JSON.stringify()ed bool command line parameters, e.g. "--extendDataset"
# See: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def printjson(type, message):
    print(json.dumps({type: message}))
    sys.stdout.flush()


def signalHandler(signal, frame):
    global closeSafe
    closeSafe = True


signal.signal(signal.SIGINT, signalHandler)
closeSafe = False

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", type=str, required=False, default="haarcascade_frontalface_default.xml",
                help="path to where the face cascade resides")
ap.add_argument("-e", "--encodings", type=str, required=False, default="model/encodings.pickle",
                help="path to serialized db of facial encodings")
ap.add_argument("-p", "--usePiCamera", type=int, required=False, default=1,
                help="Is using picamera or builtin/usb cam")
ap.add_argument("-s", "--source", required=False, default=0,
                help="Use 0 for /dev/video0 or 'http://link.to/stream'")
ap.add_argument("-r", "--rotateCamera", type=int, required=False, default=0,
                help="rotate camera")
ap.add_argument("-m", "--method", type=str, required=False, default="haar",
                help="method to detect faces (dnn, haar)")
ap.add_argument("-d", "--detectionMethod", type=str, required=False, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-i", "--interval", type=int, required=False, default=2000,
                help="interval between recognitions")
ap.add_argument("-o", "--output", type=int, required=False, default=1,
                help="Show output")
ap.add_argument("-eds", "--extendDataset", type=str2bool, required=False, default=False,
                help="Extend Dataset with unknown pictures")
ap.add_argument("-ds", "--dataset", required=False, default="dataset",
                help="path to input directory of faces + images")
ap.add_argument("-t", "--tolerance", type=float, required=False, default=0.5,
                help="How much distance between faces to consider it a match. Lower is more strict.")
args = vars(ap.parse_args())

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
printjson("status", "loading encodings + face detector...")
detector = cv2.CascadeClassifier(args["cascade"])

# initialize the video stream and allow the camera sensor to warm up
printjson("status", "starting video stream...")


pickleFile =args["encodings"]
# variable for prev names
prevNames = []

# create unknown path if needed
if args["extendDataset"] is True:
    unknownPath = os.path.dirname("dataset//unknown/")
    try:
        os.stat(unknownPath)
    except:
        os.mkdir(unknownPath)

tolerance = float(args["tolerance"])




data = pickle.loads(open(pickleFile, "rb").read())





def start(subject,message):

    #We are not doing really face recognition
    def doRecognizePerson(faceNames, fid,x, y, w, h,originalImage):
        face_img = originalImage[y:y + h+100, x:x + w+100]

        boxes = [(y, x + w, y + h, x)]
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # compute distances between this encoding and the faces in dataset
            distances = face_recognition.face_distance(data["encodings"], encoding)

            minDistance = 1.0
            if len(distances) > 0:
                # the smallest distance is the closest to the encoding
                minDistance = min(distances)

            # save the name if the distance is below the tolerance
            if minDistance < tolerance:
                idx = np.where(distances == minDistance)[0][0]
                name = data["names"][idx]
            else:
                name = "Unknown"


            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                        (0, 0,255), 1)
            y = top - 15 if top - 15 > 15 else top + 15
            # txt = name + " (" + "{:.2f}".format(minDistance) + ")"
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 1)
            
        cv2.imwrite('faces/'+str(names[0])+" ID "+str(fid)+'.jpg', face_img)

        faceNames[fid] = str(names[0])+" ID "+str(fid)


    video_capture = VideoCapture(0)
    detected_student = {}

    #variables holding the current frame number and the current faceid
    frameCounter = 0
    currentFaceID = 0

    #Variables holding the correlation trackers and the name per faceid
    faceTrackers = {}
    faceNames = {}
    rectangleColor = (0,165,255)


    while 1:        
        frame = video_capture.read()
        try:


            frame = imutils.resize(frame, width=500)
            originalImage = frame.copy()

            #Increase the framecounter
            frameCounter += 1 

            fidsToDelete = []
            for fid in faceTrackers.keys():
                trackingQuality = faceTrackers[ fid ].update( frame )

                #If the tracking quality is good enough, we must delete
                #this tracker
                if trackingQuality < 6:
                    fidsToDelete.append( fid )

            for fid in fidsToDelete:
                print("Removing fid " + str(fid) + " from list of trackers")
                faceTrackers.pop( fid , None )


            faces = None


            if args["method"] == "dnn":
                # load the input image and convert it from BGR (OpenCV ordering)
                # to dlib ordering (RGB)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb,
                                                        model=args["detectionMethod"])
                
                print(boxes)
            elif args["method"] == "haar":
                # convert the input frame from (1) BGR to grayscale (for face
                # detection) and (2) from BGR to RGB (for face recognition)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # detect faces in the grayscale frame
                rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                                minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
                
                faces = rects

                # OpenCV returns bounding box coordinates in (x, y, w, h) order
                # but we need them in (top, right, bottom, left) order, so we
                # need to do a bit of reordering
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]



            if (frameCounter % 10) == 0:



                for (_x,_y,_w,_h) in faces:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)


                        #calculate the centerpoint
                        x_bar = x + 0.5 * w
                        y_bar = y + 0.5 * h



                        #Variable holding information which faceid we 
                        #matched with
                        matchedFid = None

                        #Now loop over all the trackers and check if the 
                        #centerpoint of the face is within the box of a 
                        #tracker
                        for fid in faceTrackers.keys():
                            tracked_position =  faceTrackers[fid].get_position()

                            t_x = int(tracked_position.left())
                            t_y = int(tracked_position.top())
                            t_w = int(tracked_position.width())
                            t_h = int(tracked_position.height())


                            #calculate the centerpoint
                            t_x_bar = t_x + 0.5 * t_w
                            t_y_bar = t_y + 0.5 * t_h

                            #check if the centerpoint of the face is within the 
                            #rectangleof a tracker region. Also, the centerpoint
                            #of the tracker region must be within the region 
                            #detected as a face. If both of these conditions hold
                            #we have a match
                            if ( ( t_x <= x_bar   <= (t_x + t_w)) and 
                                    ( t_y <= y_bar   <= (t_y + t_h)) and 
                                    ( x   <= t_x_bar <= (x   + w  )) and 
                                    ( y   <= t_y_bar <= (y   + h  ))):
                                matchedFid = fid


                        #If no matched fid, then we have to create a new tracker
                        if matchedFid is None:

                            print("Creating new tracker " + str(currentFaceID))

                            #Create and store the tracker 
                            tracker = dlib.correlation_tracker()
                            tracker.start_track(frame,
                                                dlib.rectangle( x-10,
                                                                y-20,
                                                                x+w+10,
                                                                y+h+20))

                            faceTrackers[ currentFaceID ] = tracker


                            #Start a new thread that is used to simulate 
                            #face recognition. This is not yet implemented in this
                            #version :)

                            t = threading.Thread( target = doRecognizePerson ,
                                                args=(faceNames, currentFaceID,x, y, w, h,originalImage))
                            t.start()

                            #Increase the currentFaceID counter
                            currentFaceID += 1





            for fid in faceTrackers.keys():
                tracked_position =  faceTrackers[fid].get_position()

                t_x = int(tracked_position.left())
                t_y = int(tracked_position.top())
                t_w = int(tracked_position.width())
                t_h = int(tracked_position.height())

                cv2.rectangle(frame, (t_x, t_y),
                                        (t_x + t_w , t_y + t_h),
                                        rectangleColor ,2)


                if fid in faceNames.keys():
                    cv2.putText(frame, faceNames[fid] , 
                                (int(t_x + t_w/2), int(t_y)), 
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)
                                    
                else:
                    cv2.putText(frame, "Detecting..." , 
                                (int(t_x + t_w/2), int(t_y)), 
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)


            cv2.putText(frame, "Total Count: "+str(len(faceNames)) , (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            frame = imutils.resize(frame, width=1000, height=700)

            # Display the resulting image

            cv2.imshow('People Counting', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(faceNames)
                listPersons=''

                for name in faceNames:
                    listPersons  = listPersons+"\n"+faceNames[name]
                                # Define your subjects
                subject_9_to_930 = "Person Came after 9 AM and before  9:30 AM"
                subject_931_to_1245 = "Person Leaving or Coming Between 9.30 AM and before  1.00 PM"
                subject_130_to_300 = "Person Leaving  or Coming Between 1.30 PM and before  3.00 PM"
                subject_300_to_330 = "Person Leaving  or Coming Between 3.00 PM and before  3.30 PM"
                # Get the current hour
                current_time = datetime.datetime.now()

                # Get the current hour and minute
                current_hour = current_time.hour
                current_minute = current_time.minute

                # Determine the subject based on the current hour
                if current_hour == 9 and current_minute < 30:
                    email_subject = subject_9_to_930
                elif 9 <= current_hour < 13  or (current_hour == 9 and current_minute >= 30):
                    email_subject = subject_931_to_1245
                elif 13 <= current_hour < 15:
                    email_subject = subject_130_to_300
                elif current_hour == 15 and current_minute < 30:
                    email_subject = subject_300_to_330
                else:
                    # Handle cases outside the specified time ranges
                    email_subject = "PEOPLE LEAVING AND ENTERING AFTER 4"

        
                sendEmail.sendEmail(email_subject,"\n<b>Total "+str(len(faceNames))+" persons come and out </b>"+message+"\n\nDetected Peoples list\n"+listPersons)

                video_capture.release()
                cv2.destroyAllWindows()
                break
            

        except Exception as e:
            print(e)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    print('detected_student',detected_student)

