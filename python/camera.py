import time 
import threading

_LibLoaded = False
try:
    from picamera import PiCamera  # Raspberry Pi Camera
    import cv2  # OpenCV
    import face_recognition  # https://github.com/ageitgey/face_recognition 
    import argparse
    import pickle
    _LibLoaded = True
except: 
    print('[ERR]: Can not load dependency (openCV; face recognition)')

def isDepLoaded():
    return _LibLoaded
    
class Camera:
    def __init__(self, encode_face_dir, threshold=0.9):
        if not _LibLoaded:
            raise Exception('Can not load dependency (openCV; face recognition)')
        self.camera = PiCamera()
        self.threshold = threshold
        with open(encode_face_dir, "rb") as f:
            self.data = pickle.loads(f.read())
        self.name_count = {}
        for enc in self.data["names"]:
            if enc in self.data:
                self.name_count[enc] += 1
            else:
                self.name_count[enc] = 1

    def get_pic(self, file_name="temp.jpg"):
        """
        Take a photo with the camera.
        file_name: destination where the photo will be saved
        """
        self.camera.resolution = (256, 192)
        time.sleep(1)
        self.camera.capture(file_name)
        return file_name

    def authorize(self):
        """
        Take a photo with the camera and try to recognize faces
        Returns tuple in format (bool: person got recognized, str: their name) 
        """
        jpg_file_name = self.get_pic()
        image = cv2.imread(jpg_file_name)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")  # A list of tuples of found face locations in css (top, right, bottom, left) order
        encodings = face_recognition.face_encodings(rgb, boxes)  #  A list of 128-dimensional face encodings (one for each face in the image) 

        matches_name = {}#list of recognized faces
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.data["encodings"], encoding)  #  A list of True/False values indicating which known_face_encodings match the face encoding to check
            for i, match in enumerate(matches):
                if match:
                    if self.data["names"][i] in matches_name:
                        matches_name[self.data["names"][i]] += 1
                    else:
                        matches_name[self.data["names"][i]] = 1 

        for name_hit in matches_name:
            if matches_name[name_hit] > self.name_count[name_hit] * self.threshold:
                return (True, name_hit)  # returns first valid match
        return (False, "unknown")

    def async_authorize(self, success_callback=None, err_callback=None):
        """
        Same as authorize, only asinch with callbacks
        success_callback: take one argument, name of person, return nothing
        err_callback: take no argument, return nothing
        Return nothing
        """
        def f():
            result = self.authorize()
            if result[0] and success_callback != None:
                success_callback(result[1])
            elif (not result[0]) and err_callback != None:
                err_callback()               
        t = threading.Thread(target=f)
        t.setDaemon(True)   
        t.start()

if __name__ == "__main__":
    camera = Camera("outHogVal")
    camera.get_pic("0.jpg")
    print(camera.authorize())