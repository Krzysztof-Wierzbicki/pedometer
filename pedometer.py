#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def count_steps(data):
    """
    Count steps by detecting falling edge, done by smoothing data to filter out noise and finding local maximas.
    Print number of steps.
    Show maximas, smoothed and original data on a plot.
    
    Arguments: pandas.Series with measured gravitational force
    
    Returns: nothing
    """
    weight = self_weight - 1

    #smoothing
    smoothed = pd.DataFrame(columns = ['values', 'peaks'])
    for i in range(len(data)):
        try:
            value = ( np.sum( data[ i-smoothing : i+smoothing+1 ] ) + data[i]*weight )/ (2*smoothing+weight+1) 
            #mean of self_weight x self and 2 x smoothing neighbors
            smoothed = smoothed.append( {'values': value}, ignore_index = True )
        except KeyError:
            smoothed = smoothed.append({'values': None}, ignore_index = True) #when there are not enough neighbors on one of the sides
    
    #peak finding
    mean = smoothed['values'].mean()
    up = mean + threshold #upper bound

    for i, v in enumerate(smoothed['values']):
        try:
            #check if greater than left and right neaighbor and far enough from mean
            if smoothed['values'][i-1] < v and smoothed['values'][i+1] < v and v > up:
                smoothed['peaks'][i] = v
            else:
                smoothed['peaks'][i] = None
        except KeyError:
            smoothed['peaks'][i] = None

    #plot
    plt.plot(data, 'g-', label = 'input')
    plt.plot(smoothed['values'], 'k-', label = 'smoothed')
    plt.plot(smoothed['peaks'], 'ro', label = 'peaks')
    plt.xlabel('sample #')
    plt.ylabel('gravitational force [g]')
    plt.legend()
    plt.show()

    print('Number of steps: ', smoothed['peaks'].count())

#globas settings
threshold = 0.0
smoothing = 5
self_weight = 1.5

if __name__ == "__main__":
    filename = 'accelerometer.csv'

    data = pd.read_csv(filename)

    count_steps(data['g_measured'])
