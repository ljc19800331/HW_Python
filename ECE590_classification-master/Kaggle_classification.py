# Code structure
# Read the data and storage the data into an array x
# Read the data and normalize the image
# Read the label and storage into an array y
# Train the model and test the result

from skimage import io,transform
import glob
import os
import tensorflow as tf
import numpy as np
import time
import matplotlib.image as mpimg
import csv
import cv2

def read_images(path, N_region):

    # load the labels
    with open('stage1_labels.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lables = []
        name_region = []
        for row in spamreader:
            lables.append(row)

    lables.pop(0)

    y_lable = []
    images = []
    images_check = []
    ID_names = []
    w = 100
    h = 100
    c = 3

    for j in range(len(os.listdir(path))):
        filename = os.listdir(path)[j]
        id_name = filename.split('_')[0]
        img = mpimg.imread(os.path.join(path, filename))
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        match_name_1 = id_name  # ID_names[j]
        for i in range(len(lables)):
            match_name_2 = lables[i][0].split('_')[0]
            idx_lable = int(lables[i][0].split('_')[1].split(',')[1])
            idx_region = int(lables[i][0].split('Zone')[1].split(',')[0])
            if match_name_1 == match_name_2 and idx_region == N_region:
                # print('The match name 1 is ', match_name_1)
                # print('The match name 2 is ', match_name_2)
                # print('The j is ', j)
                # print('The i is ', i)
                ID_names.append(id_name)
                y_lable.append(idx_lable)
                img = transform.resize(img, (w, h))
                images.append(img)

    return images, y_lable

time_start = time.clock()
w = 100
h = 100
c = 3
#N_region = 1
#data,label = Kaggle_classification.read_images(path)

data_1 = [] # train loss
data_2 = [] # train accuracy
data_3 = [] # validation loss
data_4 = [] # validation accuracy

for flag_region in range(16):

    Train_loss = []
    Train_acc = []
    Validate_loss = []
    Validate_acc = []

    flag_region += 1
    N_region = flag_region
    print('The current region number is ', N_region)
#N_region = int(input('The index of region is '))
    path = 'C:/Users/maguangshen/PycharmProjects/ECE590/ECE590/dataset/' + str(N_region)
    print('The current path is ', path)
    data,label = read_images(path,N_region)

    data_train = np.asarray(data, np.float32)
    label_train = np.asarray(label,np.int32)

    # randomly distribute the data
    num_example = data_train.shape[0]
    arr = np.arange(num_example)
    np.random.shuffle(arr)
    data_use = data_train[arr]
    label_use = label_train[arr]

# Divide into training and testing sets 8/2 ratio
    ratio = 0.8
    s = np.int(num_example*ratio)
    x_train = data_use[:s]
    y_train = label_use[:s]
    x_val=data_use[s:]
    y_val=label_use[s:]

# Train the model
    x = tf.placeholder(tf.float32,shape=[None,w,h,c],name='x')
    y_= tf.placeholder(tf.int32,shape=[None,],name='y_')

# The first layer
    conv1=tf.layers.conv2d(
          inputs=x,
          filters=32,
          kernel_size=[5, 5],
          padding="same",
          activation=tf.nn.relu,
          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    pool1=tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

# The second layer
    conv2=tf.layers.conv2d(
          inputs=pool1,
          filters=64,
          kernel_size=[5, 5],
          padding="same",
          activation=tf.nn.relu,
          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    pool2=tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

# The third layer
    conv3=tf.layers.conv2d(
          inputs=pool2,
          filters=128,
          kernel_size=[3, 3],
          padding="same",
          activation=tf.nn.relu,
          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    pool3=tf.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2], strides=2)

# The fourth layer
    conv4=tf.layers.conv2d(
          inputs=pool3,
          filters=128,
          kernel_size=[3, 3],
          padding="same",
          activation=tf.nn.relu,
          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    pool4=tf.layers.max_pooling2d(inputs=conv4, pool_size=[2, 2], strides=2)

    re1 = tf.reshape(pool4, [-1, 6 * 6 * 128])

# Fully connected layer
    dense1 = tf.layers.dense(inputs=re1,
                          units=1024,
                          activation=tf.nn.relu,
                          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                          kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))
    dense2= tf.layers.dense(inputs=dense1,
                          units=512,
                          activation=tf.nn.relu,
                          kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                          kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))
    logits= tf.layers.dense(inputs=dense2,
                            units=5,
                            activation=None,
                            kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                            kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))

# optimization the loss function
    loss=tf.losses.sparse_softmax_cross_entropy(labels=y_,logits=logits)
    train_op=tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)
    correct_prediction = tf.equal(tf.cast(tf.argmax(logits,1),tf.int32), y_)
    acc= tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Batch size
# def minibatches
    def minibatches(inputs = None, targets = None, batch_size = None,shuffle = False):
        assert len(inputs) == len(targets)
        if shuffle:
            indices = np.arange(len(inputs))
            np.random.shuffle(indices)
        for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)
            yield inputs[excerpt], targets[excerpt]

    # Train the model
    n_epoch=10
    batch_size=64
    sess=tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    for epoch in range(n_epoch):

        #start_time = time.time()
        time_start = time.clock()

        # training
        train_loss, train_acc, n_batch = 0, 0, 0
        for x_train_a, y_train_a in minibatches(x_train, y_train, batch_size, shuffle=True):
            _, err, ac = sess.run([train_op, loss, acc], feed_dict={x: x_train_a, y_: y_train_a})
            train_loss += err;
            train_acc += ac;
            n_batch += 1
        print("   train loss: %f" % (train_loss / n_batch))
        Train_loss.append((train_loss / n_batch))
        print("   train acc: %f" % (train_acc / n_batch))
        Train_acc.append((train_acc / n_batch))

        # validation
        val_loss, val_acc, n_batch = 0, 0, 0
        for x_val_a, y_val_a in minibatches(x_val, y_val, batch_size, shuffle=False):
            err, ac = sess.run([loss, acc], feed_dict={x: x_val_a, y_: y_val_a})
            val_loss += err;
            val_acc += ac;
            n_batch += 1
        print("   validation loss: %f" % (val_loss / n_batch))
        Validate_loss.append((val_loss / n_batch))
        print("   validation acc: %f" % (val_acc / n_batch))
        Validate_acc.append((val_acc / n_batch))
        time_elapsed = (time.clock() - time_start)
    sess.close()

    data_1.append(Train_loss)
    data_2.append(Train_acc)
    data_3.append(Validate_loss)
    data_4.append(Validate_acc)

    time_elapsed = (time.clock() - time_start)
    print('The total time is ', time_elapsed)
    print("Finish the %f region" % (N_region))

thefile = open('Train_loss_1.txt', 'w')
for item in data_1:
    #for item_1 in item:
    thefile.write("%s\n" % item)
thefile.close()

thefile = open('Train_acc_1.txt', 'w')
for item in data_2:
    thefile.write("%s\n" % item)
thefile.close()

thefile = open('Validate_loss_1.txt', 'w')
for item in data_3:
    thefile.write("%s\n" % item)
thefile.close()

thefile = open('Validate_acc_1.txt', 'w')
for item in data_4:
    thefile.write("%s\n" % item)
thefile.close()

# Read the image
# import Kaggle_classification
# from Kaggle_classification import *

# img_test = images[10]
# cv2.imshow('image', img_test)

# #path = 'C:/Users/maguangshen/PycharmProjects/ECE590/ECE590/flower_photos/flower_photos/'
# test_filename = os.listdir(path)[1]
# test_id_name = test_filename.split('_')[0]
# test_img = mpimg.imread(os.path.join(path, test_filename))
# test_img = transform.resize(test_img, (100, 100))
# test_rgb = tf.image.grayscale_to_rgb(test_img)
# tf.image.decode_png(os.path.join(path, test_filename),  channels=3)
#
# backtorgb = cv2.cvtColor(test_img,cv2.COLOR_GRAY2RGB)
# cv2.imshow('image', backtorgb)

# Check the result of each image, show in a 4 by 4 plot platform
# img_check = data[60]
# cv2.imshow('image', img_check)
# tf.image.grayscale_to_rgb(img_check)

# img_normalized = tf.image.per_image_standardization(img_check)  # 3 channel
# tf.per_image_standardization(img_check)