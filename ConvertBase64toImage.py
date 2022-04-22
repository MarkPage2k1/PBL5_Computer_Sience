import urllib.request
from PIL import Image
def ConverBase64toImage(base64_code):
    fileName = 'test.jpeg'
    URLImage = base64_code
    urllib.request.urlretrieve(URLImage, fileName)
    img = Image.open(fileName)