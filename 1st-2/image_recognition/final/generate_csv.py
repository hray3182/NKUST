import scipy.io as sio
import csv
import numpy as np
import re


mat = sio.loadmat('./archive/cars_annos.mat')

class_names = mat['class_names']


hash = {}

for data in class_names[0]:
    brand = data[0].split()[0]
    hash[str(data.dtype)] = brand

for i in range(len(class_names[0])):
    brand = class_names[0][i][0].split()[0]
    hash[i+1] = brand


def create_csv(filename):
    with open(f"{filename}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["image", "brand", "brand_id"]

        writer.writerow(field)

        mat = sio.loadmat(filename)

        annotations = mat['annotations']

        for annotation in annotations[0]:
            fname = annotation[5][0]
            tp = int(annotation[4][0])
            writer.writerow([fname, hash[tp], tp])


data_file_names = ["./archive/cars_train_annos.mat",
                   "./archive/cars_test_annos_withlabels.mat"]
for name in data_file_names:
    create_csv(name)
