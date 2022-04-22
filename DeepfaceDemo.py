from ast import Pass
import cv2
import matplotlib.pyplot as plt
from deepface import DeepFace
import time

# img = cv2.imread('facedetection.jpg')
try:
    pre = DeepFace.analyze(img_path = "test.jpg", actions = ['emotion'])
    print(pre["dominant_emotion"])
except:
    print('No Face !!!')

time.sleep(2)

