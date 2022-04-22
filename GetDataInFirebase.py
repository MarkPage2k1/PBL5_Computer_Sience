import re
from firebase import firebase
import time
from ConvertBase64toImage import ConverBase64toImage as B64I
afirebase = firebase.FirebaseApplication('https://pbl5-arduino-default-rtdb.firebaseio.com/', None)
result = afirebase.get('/test', None)
B64I(result['image_encode'])