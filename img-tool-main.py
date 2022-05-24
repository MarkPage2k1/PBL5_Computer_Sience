import icrawler
import cv2
import os
from icrawler.builtin import GoogleImageCrawler
import numpy as np
# crawl image from Google image
'''
google_crawler = GoogleImageCrawler(storage={'root_dir': 'baby image'})
google_crawler.crawl(keyword='baby image', max_num=10)'''

path='E:\\1\\code\\PBL5_Computer_Sience\\baby image\\000002.jpeg'
image = cv2.imread(path)
image = cv2.resize(image, (500, 500))
window_name = 'Image'
# Using cv2.cvtColor() method
# Using cv2.COLOR_BGR2GRAY color space
# conversion code
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Displaying the image 
cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows()