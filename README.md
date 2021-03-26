# Autonomous Car project


this project is for generating a model of an autonomous car in a Udacity's car simulation using convolutional neural networks


# Motivation

I honestly started this project because I was bored and I had nothing better to do

# Requirements

for this version you need to install the [udacity/self-driving-sim](https://github.com/udacity/self-driving-car-sim) it is also recommended that you install version 2 since it is the version that I have used for this project

it is also very important that you have all the required libraries and that you install the simulation in the same directory as the code file

# How to Use

after extracting the simulation in the same file as the project create an empty file which you should name (Simulation_data) then run the simulation and select the Training mode
then select the (Simulation_data) folder then run the [training.py](https://github.com/UndeadZed/Equus/blob/main/git-Equus/training.py) file notice that this will take some time as it trains your model afterwards you'll see a file in the same directory by the name (Alastor.h5) this is your model so you only have to run the [training.py](https://github.com/UndeadZed/Equus/blob/main/git-Equus/training.py) once then open the simulation and select the map and select autonomous mode then run the [Test_model.py](https://github.com/UndeadZed/Equus/blob/main/git-Equus/Test_model.py) file which should run the simulation autonomously

# Credits

this model is based on Nvidia's End-to-End Deep Learning for Self-Driving Cars which you can check from [here](https://developer.nvidia.com/blog/deep-learning-self-driving-cars/)

this was also inspired by [Murtaza Hassan's](https://github.com/murtazahassan) project on the same topic

# Screenshots
I tested it in 2 maps to see how well the model generalized

[![Screenshot-1.png](https://i.postimg.cc/C5CBnQX6/Screenshot-3.png)](https://postimg.cc/sGXDtwVp)

[![Screenshot-2.png](https://i.postimg.cc/wvXTws21/Screenshot-4.png)](https://postimg.cc/ftbNLy6s)


# Future updates

The next version will use [CARLA Simulator](https://carla.org/) and will have a more updated and specific architecture for the model that it generates which will hopefully produce better predictions and results

# Final notes

for any problems you find you can contact me directly on github
