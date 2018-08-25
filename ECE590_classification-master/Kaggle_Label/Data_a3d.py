import Data_extraction
from Data_extraction import *
import sys
from Data_extraction import *
from read_binary import *

## notice: before using this file, since it imports the read_binary module, which includes the part "im_fpath = sys.argv[1]", search
# on Google about the usage of "sys.argy", which will be used in the cmd(windows) or others in other systems.
# This script is based on the module of "read_binary"

def A3d2Mat(filepath, dirpath):
    # Convert the '.a3d' file to the npy file that can be read by MATLAB
    data_obj = data_divide(filepath)
    # save data files -- from '.a3d' to '.npy' file
    num_files = input('The number of files is')
    for i in range(int(num_files)):
        datapath = filepath + data_obj.name[i*2] + '.a3d'
        print(i)
        data = read_data(datapath)
        savepath = dirpath + data_obj.name[i*2]
        np.save(savepath, data)
    return data_obj

#def Getcsv(filepath):

def main():
    #change 1: add the path to the directory of the code
   sys.path.append('C:/Users/maguangshen/PycharmProjects/TSA_Classification-segAndCube/Kaggle_Label/')
    #change 2: change the filepath to the directory that you save all the npy data
   filepath = 'G:/Kaggle_a3d/'         ## change this by user -- the dir that you use for the original data
    #change 3: Create a new directory and change the 'dirpath' to the new directory
   dirpath = 'G:/Kaggle_npy/'      ## change this by user -- the dir that you save the data to
   #First:Get the csv files
   obj = data_divide(filepath)
   name_array = obj.name
   label_array = obj.label
   zone_array = obj.zone
   ## Notice, this is based on python 3.6, look for the tutorial for input and output of csv.file if for other version
   # Problem: not working for python 2.7
    # change 4: change the name 'example' and the path directory as you want
   with open('C:/Users/maguangshen/PycharmProjects/TSA_Classification-segAndCube/Kaggle_Label/KaggleLabel.csv','w') as csvfile:
       spamwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
       spamwriter.writerow(name_array)
       spamwriter.writerow(label_array)
       spamwriter.writerow(zone_array)
   data_obj = A3d2Mat(filepath, dirpath)

if __name__ == '__main__':
    main()
