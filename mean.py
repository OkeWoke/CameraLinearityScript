# Linearity Tester
"""This script takes a directory of images that has exposure time encoded in its name and plots mean adu vs time"""

from PIL import Image
from scipy import stats

import matplotlib.pyplot as plt
import numpy as np
import time, re, glob, os

DIRECTORY = "C:\\Users\\Liam\\ownCloud\\LinearityTest\\LIGHT" #Directory containing all image files

def timer(func):
    """Takes a function, returns the time duration for execution of the function and any output from function"""
    start = time.time()
    a = func()
    end = time.time()
    return (end-start,a)

def mean(im):
    """Takes image object, returns mean value of image"""
    mean  = sum(list(im.getdata())) / (im.width*im.height)
    return mean

def getExposure(filename):
    """Takes string name of file, returns exposure time of image embdedded in filename using specific regex"""
    a = re.search('NaN_(.+?)s_', filename)
    if a:
        return float(a.group(1))

meanArray = []
expTimeArray = []

os.chdir(DIRECTORY)
for file in glob.glob("*.tif"):
    image = Image.open(file)    
    expTime = getExposure(file)
    meanADU  = mean(image)
    if expTime in expTimeArray: #if already added datapoint for a given exp time, avg it.
        i = expTimeArray.index(expTime)
        meanArray[i]+=meanADU
        meanArray[i]/=2
    else:#else add new entries into arrays.
        meanArray.append(meanADU)
        expTimeArray.append(expTime)
    
#y=mx+c
#Slope, Intercept, correlation coef, pval for hyp test, standard error
m, c, r_value, p_value, se = stats.linregress(expTimeArray,meanArray)

xLinSpace= np.linspace(0,300,100)

yFit = m*xLinSpace + c
plt.figure(0)
plt.xlabel("Exposure Time (s)")
plt.ylabel("Mean Pixel Value ADU")
plt.title("Linearity of Canon 60D")

plt.plot(expTimeArray,meanArray,marker='.',linestyle="None")
plt.plot(xLinSpace,yFit,linestyle="solid")

print("R-Square: ",r_value**2)
print("ADU/Sec: ",m)
print("intercept: ",c)
plt.savefig("plot.pdf")

residuals = []
for i in range(0,len(expTimeArray)):
    residuals.append((((meanArray[i]-c)/expTimeArray[i])-m)/m)
    
plt.figure(1)
plt.title("Residual Deviation")
plt.xlabel("Exposure Time (s)")
plt.ylabel("Deviation %")
plt.plot(expTimeArray[:-1],residuals[:-1])
plt.savefig("plot2.pdf")