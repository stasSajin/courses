import face_recognition
import sys

def face_detector2(img_path):
    image = face_recognition.load_image_file(img_path)
    try:
        result = len(face_recognition.face_locations(image, model='cnn')) > 0 
    except RuntimeError:
        result = len(face_recognition.face_locations(image)) > 0 
    return result


print(face_detector2(sys.argv[1]))
