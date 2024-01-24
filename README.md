# Planet Hunting with Python

## Introduction

This is a repository that builds on provided code from QMUL. We analyse data sent from NASA's Kepler spacecraft 
## Next steps

- plot models to data, optimise accuracy of the models
- draw conclusions about them, analyse how big they are, how many planets in a system perhaps

## What this repository contains

- Module for finding planet parameters
- Module for plotting piece wise function (line of best fit) | in progress
- Module for Chi-squared test
- Module for extension tasks | planned

## List of files

## utils.py
- Imports
floor and ceil from math
- Functions
binarySearch()
    * Parameters : array, element
    * finds an item in a sorted array using a binary search method
    * O(log n) time complexity
    * returns the location of the element in the array
interpolationSearch()
    * Parameters : array, element
    * finds an item in a sorted array using a interpolation search method
    * O(log log n) time complexity - an improvement on binary search
    * returns the location of the element in the array

## utils_test.py
- Imports
the information / functions from utils.py
perf_counter from time
random
numpy
- Functions
benchmarkArrayFunc()
    * Parameters : size (size of the array created), n (number of times each search is performed), funcs(the functions to be tested)
    * compares the average time of different inputted functions
    * O(n²)
    * returns the name of the function and average time in milliseconds for each of the functions inputted

## test.py
- Imports
DataAnalyser from data_analyser
perf_counter from time
- Classes
Timing()
- Functions (inside class - Timing())



## pwlf.py
piecewise linear library -- not our code but referred to in other parts of the project

## data_analyser.py
- Imports
stdev from statistics
floor and ceil from math
AbstractDataHandler and LocalDataHandler from data_handler
matplotlib.pyplot
numpy
PiecewiseLinFit from pwlf.py
- In class DataAnalyser -- __init__
self.handler
self.times
self.flux
self.phaseFoldedTime
self.radius
self.mass
self.size
self.period
self.transitBound
self.transitLength
self.phase
self.dt
- In class DataAnalyser -- Functions
plot()
    * Parameters : self, plotType=""
    * plots graphs of two case types - a regular scatter plot of times against flux and a phase folded graph that calls another function __getPhaseFoldedTime() and plots the returned value against flux.