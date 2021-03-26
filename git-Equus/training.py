print('setting up')
from sklearn.utils import validation
from utils import *
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt





#In the first step we import the collected data
path = 'Simulation_data'
data = Import_data(path)

#The second step we Visualize and balance the data to ensure that the training process is not biased


#Balance_data(data,True)#set the second parameter as True to visualize the data


#third step is where we put the images in a list and the steering angle in another list
Images_path,steering = load_data(path,data)
print(Images_path[0],steering[0])

#the fourth step is splitting up the data into training and validation

x_train,x_val,y_train,y_val =train_test_split(Images_path,steering,test_size=0.2,random_state=5)
print("the total Training data :",len(x_train))
print("the total validation data:",len(x_val))

#the fifth step is creating our model
model = create_model()
model.summary()

#the sixth step and the main step is training our model

model.fit(batchGenerator(x_train,y_train,100,1),steps_per_epoch = 300,epochs=10,validation_data=batchGenerator(x_val,y_val,100,0),validation_steps=200)

#the last step is saving the model
model.save("Alastor.h5")
print('model successfully saved')
