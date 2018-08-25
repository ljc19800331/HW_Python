import numpy as np
import matplotlib.pyplot as plt
import random
import time

plt.ion()       # Enable interactive mode
fig = plt.figure()  # Create figure
axes = fig.add_subplot(111) # Add subplot (dont worry only one plot appears)

axes.set_autoscale_on(True) # enable autoscale
axes.autoscale_view(True,True,True)

l, = plt.plot([], [], 'r-') # Plot blank data
plt.xlabel('x')         # Set up axes
plt.title('test')

k = 5
xdata=[0.5 for i in range(k+1)]     # Generate a list to hold data
ydata=[j for j in range(k+1)]

#while True:
time_start = time.clock()
for i in range(100):
    #y = float(raw_input("y val :")) #Get new data
    ydata = random.sample(range(1, 100), 50)
    xdata = random.sample(range(1, 100), 50)
    #y = random.randint(1, 100)
    #xdata.append(y)     # Append new data to list
    #k = k + 1       # inc x value
    #ydata.append(k)
    l.set_data(ydata,xdata) # update data
    #print xdata     # Print for debug perposes
    #print ydata
    axes.relim()        # Recalculate limits
    axes.autoscale_view(True,True,True) #Autoscale
    plt.pause(0.001)
    plt.draw()      # Redraw
time_elapsed = (time.clock() - time_start)
print('The time elapsed is', time_elapsed)