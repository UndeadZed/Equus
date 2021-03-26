from imgaug.imgaug import flatten
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.image as mpimg
from imgaug import augmenters as iaa
import cv2
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D,Flatten,Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.engine import sequential


segment = '\n=================================================================\n'
#This is a function that splits the name of the image from the path
def Get_name(filepath):
    return filepath.split("\\")[-1]



#this is the function which imports the data from the simulation
def Import_data(path):
    coloums = ['Center','Left','Right','Steering','Throttle','Brake','Speed']
    data = pd.read_csv(os.path.join(path,'driving_log.csv'),names = coloums)
    #print(get_name(data['Center'][0]))
    data['Center'] = data['Center'].apply(Get_name)
    #print(data.head())
    print("the total number of data we have is: ",data.shape[0])
    return data

#This is the function responsible for balancing and visualizing the data
def Balance_data(data, display=True):
    nBins = 31
    samplesPerBin = 1000
    hist, bins = np.histogram(data['Steering'],nBins)
    #print(bins)
    center = (bins[:-1]+bins[1:])*0.5
    if display:
        print(segment)
        print (center)
        plt.bar(center,hist,width = 0.06)
        plt.plot((-1,1),(samplesPerBin,samplesPerBin))
        plt.show()
    remove_index_list = []
    for i in range(nBins):
        binDataList = []
        for j in range(len(data['Steering'])):
            if data['Steering'][j] >= bins[i] and data['Steering'][j] <= bins[i+1]:
                binDataList.append(j)
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samplesPerBin:]
    remove_index_list.extend(binDataList)
    print("the removed images are = ",len(remove_index_list))
    data.drop(data.index[remove_index_list],True)
    print('the remaining images : ', len(data))
    if display:
        hist,_ = np.histogram(data['Steering'],nBins)
        plt.bar(center,hist,width = 0.06)
        plt.plot((-1,1),(samplesPerBin,samplesPerBin))
        plt.show()

    
#this is the function that loads the data
def load_data(path, data):
    Images_path = []
    steering = []

    for i in range(len(data)):
        indexedData = data.iloc[i]
       # print(indexedData)
        Images_path.append(os.path.join(path,'IMG',indexedData[0]))
        steering.append(float(indexedData[3]))

    Images_path = np.array(Images_path)
    steering = np.array(steering)
    return Images_path,steering

#this is a function that augments the images to get more data

def augmentImage(imgpath,steering):
    img = mpimg.imread(imgpath)
    #first we start with the pan
    if np.random.rand()<0.5:
        pan = iaa.Affine(translate_percent={'x':(-0.1,0.1),'y':(-0.1,0.1)})
        img = pan.augment_image(img)

    #now we change the zoom
    if np.random.rand()<0.5:
        zoom = iaa.Affine(scale = (1,1.2))
        img = zoom.augment_image(img)

    #Now we change the brightness
    if np.random.rand()<0.5:
        brightness = iaa.Multiply((0.4,1.2))
        img = brightness.augment_image(img)

    #lastly we flip the image
    if np.random.rand()<0.5:
        img = cv2.flip(img,1)
        steering = -steering




    return img,steering

def preProcessing(img):
    img = img[60:135,:,:]
    img = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.resize(img,(200,66))
    img = img/255
    return img

def batchGenerator(img_path,steeringList,batch_size,flag):
    while True:
        img_batch = []
        steering_batch = []
        for i in range(batch_size):
            index = random.randint(0,len(img_path)-1)
            if flag:
                img, steering = augmentImage(img_path[index],steeringList[index])
            else:
                img = mpimg.imread(img_path[index])
                steering = steeringList[index]
            img = preProcessing(img)
            img_batch.append(img)
            steering_batch.append(steering)
        yield (np.asarray(img_batch),np.asarray(steering_batch))





def create_model():

    model = Sequential()

    model.add(Convolution2D(24,(5,5),(2,2),input_shape=(66,200,3),activation='elu'))
    model.add(Convolution2D(36,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(48,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))

    model.add(Flatten())
    model.add(Dense(100,activation='elu'))
    model.add(Dense(50,activation='elu'))
    model.add(Dense(10,activation='elu'))
    model.add(Dense(1))

    model.compile(Adam(learning_rate=0.0001),loss= 'mse')
    return model




#!!!!!!!!!!!!!!!!!!!!!this part is for testing only!!!!!!!!!
#img = mpimg.imread('test.jpg')
#imgRe = preProcessing(img)
#plt.imshow(imgRe)
#plt.show()

    