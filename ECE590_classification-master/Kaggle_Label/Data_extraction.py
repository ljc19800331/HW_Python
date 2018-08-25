import os
import csv

# This script has the following functions:
# 1.Design a class called object(i.e the file of a person) that includes information of object name, zone, label
# 2.Divide the file name into several part: Person's name, Zone number, label value. e.g in the csv file, some of the name
# is "0043db5e8c819bffc15261b1f1ac5e42_Zone1,1" -- "0043db5e8c819bffc15261b1f1ac5e42" + "1" + "1"(label), all this information is
# saved in a new csv.file

def file_name(filepath):     ## filepath here is the directory that save the original '.a3d file', e.g 'D:/Kaggle_Data/'
    # read the name of the object and remove the string '.a3d' from the name
    # e.g "0f47335091ce43a8025ebd2076630dfd.a3d" -- "0f47335091ce43a8025ebd2076630dfd" + ".a3d"
    filename = []
    for root, dirs, files in os.walk(filepath):
        print(files)
        for file in files:
             filename.append(os.path.splitext(file)[0])
    return filename

def Object_Name_Zone():
    #  change 5: change the directory to the 'Stage1_Label.csv' location
    #  read the csv.file downloaded from server, change the path name to the directory that you save 'Stage1_LabeL.csv' from server
    with open('C:/Users/maguangshen/PycharmProjects/TSA_Classification-segAndCube/Kaggle_Label/stage1_labels.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        object_label = [row[1] for row in reader]
    with open('C:/Users/maguangshen/PycharmProjects/TSA_Classification-segAndCube/Kaggle_Label/stage1_labels.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        object_name = [row[0] for row in reader]
    return object_name, object_label

def data_divide(filepath):      ### e.g filepath = 'G:/Kaggle_a3d/'
    # Divide the name with "object name", "zone name", "label value", read the "stage1_labels.csv"
    t1 = object([],[],[],[])
    #Generate the interval vector, this is only used to seperate the object name, see the result of the csv.file
    t_interval = []
    for i in range(16):
        t_interval.append(' ')
    File_name = file_name(filepath) # the name includes only the name of the object
    objectname, objectlabel = Object_Name_Zone() # the name includes region and label
    #for file in File_name:
    for i in range(len(File_name)):
        #FilePath = filepath + File_name[i] + '.a3d'
        #check if the filename in label is the same as it in the current name
        flag = 0
        for j in range(len(objectname)):                              # objfile = '0d10b14405f0443be67a75554da778a0z_zone8'
            file_zone = objectname[j][::-1].split('_',1)[-1][::-1]    # e.g give '0d10b14405f0443be67a75554da778a0z'
            file_test = objectname[j][::-1].split('_',1)[0][::-1]     # e.g give '8', also consider the problem of '10' or '11'
            file_zonelabel = file_test[::-1].split('e',1)[0][::-1]
            #find the index position of value -- for labeling the result
            if file_zone == File_name[i]:
                #print('The same')
                index_obj = objectname.index(objectname[j])
                value_label = objectlabel[index_obj]
                t1.label.append(value_label)
                t1.zone.append(file_zonelabel)
                flag += 1
        if flag != 0:
            t1.name.append(File_name[i])
            t1.name.append(t_interval)

    #print(t1.name)
    return t1

class object:
    def __init__(self, data, name, zone, label):
        self.data = data
        self.name = name
        self.zone = zone
        self.label = label
