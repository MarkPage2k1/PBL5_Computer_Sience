import icrawler
import cv2
import os
from icrawler.builtin import GoogleImageCrawler
import numpy as np
# crawl image from Google image
'''f = open("E:\\1\\code\\PBL5_Computer_Sience\\babyimagegray\\test.txt",'r',encoding = 'utf-8')
list_image = f.readlines()
list_old = list_image[:]
f.close()'''
google_crawler = GoogleImageCrawler(storage={'root_dir': 'babyimage'})
google_crawler.crawl(keyword='baby image', max_num=100)

raw_path=r'E:\\1\\code\\PBL5_Computer_Sience\\babyimage\\' 
window_name = 'Image'
save_path=r"E:\\1\\code\\PBL5_Computer_Sience\\babyimagegray"

img_folder = os.listdir(raw_path)
print(img_folder)

for j in range(len(img_folder)):
    path = os.path.join(raw_path, img_folder[j])
    image = cv2.imread(path)
    if image is None:
        print('Wrong path:', path)
    else:
        print("0")
    path=raw_path
    image = cv2.resize(image, dsize=(500,500))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #if img_folder[j].split('.')[0] not in list_image:
    os.chdir(save_path) 
    filename = img_folder[j]
    cv2.imwrite(filename,image) 
    print("save_path")  
    print(os.path.join(save_path,img_folder[j]))  
'''list_image.append(img_folder[j].split('.')[0])
print(list_image)
with open(r'E:\\1\\code\\PBL5_Computer_Sience\\babyimagegray\\test.txt', 'w') as fp:
    for item in list_image:
        # write each item on a new line
        if item not in list_old:
            fp.write("%s\n" % item)
    print('Done')
    
'''
 
''' image=cv2.imshow("window_name", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''     
