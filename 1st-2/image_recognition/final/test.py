import scipy.io as sio
import csv
import numpy as np
import re


mat = sio.loadmat('./archive/cars_annos.mat')
annotations = mat['annotations']
annotations = np.transpose(annotations)
class_names = mat['class_names']


hash = {}

# for data in class_names[0]:
#     # print(data.dtype, data[0])
#     # hash[data.dtype] = " ".split(data[0])[0]
#     brand = data[0].split()[0]
#     print(re.findall(r'\d+', str(data.dtype))[0])
#     hash[str(data.dtype)] = brand

for i in range(len(class_names[0])):
    brand = class_names[0][i][0].split()[0]
    hash[i+1] = brand

# print(hash)

def create_csv():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["image", "brand", "brand_id"]
        
        writer.writerow(field)

        train_count = 0
        test_count = 0
            
        for annotation in annotations:
            # regex: \d{6}.jpg
            # fname = annotation[0][0][0]
            # fname = re.findall(r'\d{6}.jpg', fname)[0]
            is_test = annotation[0][6][0][0]
            fname = "archive/"
            if is_test == 1:
                test_count += 1
                fname += f"cars_test/cars_test/{test_count:05d}.jpg"
            else:
                train_count += 1
                fname += f"cars_train/cars_train/{train_count:05d}.jpg"
            tp = int(annotation[0][5][0][0])
            writer.writerow([fname, hash[tp], tp])


create_csv()



