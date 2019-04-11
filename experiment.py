# -*- coding: utf-8 -*- 
import os
import sys
import math
import numpy as np 
import matplotlib.pyplot as plt

cwd = os.getcwd()
dataFolder = os.path.join(cwd, "data")

print("Path Data : %s" %(dataFolder))

timeData = []
hallData = []
currentData = []
planarVoltData = []
kalman_hallData = []
kalman_currentData = []
kalman_planarVoltData = []
calculated_mag = []

def fileLoad():
    relPath = "./data"
    while(True):
        print('\n\n' + "="*50)
        file_name = input("\n\n\t\tChoose Raw Data\n\tex]test_0.1\n\n")
        file_name = file_name + ".txt"
        filePath = os.path.join(dataFolder, file_name)
        relFilePath =  os.path.join(relPath, file_name)
        print(filePath)
        if os.path.isfile(filePath) is True:
            print("File : %s LOADED" %(file_name))
            f = open(relFilePath, "r")
            _lineTrash = f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                dataLine = line.split()
                #print(dataLine)
                timeData.append(float(dataLine[1])/1000)
                currentData.append(float(dataLine[2]))
                #FIXME
                hallData.append(float(dataLine[5]))
                planarVoltData.append(float(dataLine[4]))
            f.close()
            break
        else:
            print('\n' + "!!!!Input Error!!!!" + '\n')
            pass 

def rawMeanFix(rawData):
    _result = []
    # FIXME
    meanIdx = 25
    noise = 0
    for idx in range(meanIdx):
        noise = noise + rawData[idx]
    noise = noise / meanIdx
    
    for idx in range(1, len(rawData)-1):
        rawData[idx] = rawData[idx] - noise
        '''
        if not idx == 0 or idx == len(rawData):
            mean = (rawData[idx-1] + rawData[idx+1])/2
            if abs(rawData[idx]-mean) > mean:
                rawData[idx] = mean
        '''
    #return result

def plotScatter(xList, yList, *args):
  argsList = []
  for arg in args:
    argsList.append(arg)

  fig, ax = plt.subplots()
  ax.set_xlabel(argsList[0])
  ax.set_ylabel(argsList[1])
  ax.plot(xList, yList,'o')
  plt.show()

def plotdiffScales(xList, y1, y2, *args):
  argsList = []
  for arg in args:
    argsList.append(arg)

  fig, ax1 = plt.subplots()
  color1 = "tab:red"
  ax1.set_xlabel(argsList[0])
  ax1.set_ylabel(argsList[1], color=color1)
  ax1.plot(xList, y1, color=color1)
  ax1.tick_params(axis='y', labelcolor=color1)

  ax2 = ax1.twinx()
  color2 = "tab:blue"
  ax2.set_ylabel(argsList[2], color=color2)
  ax2.plot(xList, y2, color=color2)
  ax2.tick_params(axis='y', labelcolor=color2)
  fig.tight_layout()
  plt.show()

def inducedV(turn, outerL, inductance, dBdt):
    D = outerL # [m]
    inc_B = dBdt # [T/sec]
    L = inductance # [H]
    result = 0
    for i in range(turn):
        D = D - i * 2 * (0.25e-3)
        A = math.pow(D, 2)
        result = result + A*inc_B
    return result

def magCalc(tData, vData, turn, outerL, inductance):
    magRelative = 0 # Relative magnetic field intensity
    for idx, val in enumerate(vData):
        if idx == 0:
            calculated_mag.append(0)
        else:
            #indV_diff = val - vData[idx-1]
            t_diff = tData[idx] - tData[idx-1]
            #FIXME
            # + or - depending on the raw data sign
            magRelative = magRelative - val*t_diff / (turn * math.pow(outerL,2))
            calculated_mag.append(magRelative)


class KalmanFilter():
    # REF
    # https://core.ac.uk/download/pdf/20641186.pdf
    def __init__(self, process_noise, sensor_noise, estimated_error, initial_value):
        self.q = process_noise # process noise covariance
        self.r = sensor_noise # measurement noise covariance
        self.x = estimated_error # value
        self.p = initial_value # estimation error covariance
        self.k = 0 # kalman gain

    def getFiltered(self, measurement):
        self.p = self.p + self.q
        self.k = self.p / (self.p + self.r)
        self.x = self.x + self.k * (measurement - self.x)
        self.p = (1-self.k)* self.p
        print("P : %f K : %f X : %f " %(self.p, self.k, self.x))

        return self.x

    def setParameters(self, process_noise, sensor_noise, estimated_error):
        self.q = process_noise
        self.r = sensor_noise
        self.p = estimated_error

    def meanFix(self, filteredList):
        minData = 0
        #FIXME
        biasIdx = 23 # idx of the data list to move mean of the data
        for i in range(biasIdx):
            minData = minData + filteredList[i]
        minData = minData / biasIdx

        for idx, data in enumerate(filteredList):
            temp = data - minData
            filteredList[idx] = temp 


if __name__ == "__main__":
    # Execute only if run as a script 
    fileLoad()
    filteredMeasurement = 0
    #FIXME
    rawMeanFix(planarVoltData)
    #FIXME
    p_noise = 0.0125 # 0.0125 for low ramping, 0.125 for 1A/sec 2A/sec
    s_noise = 32
    e_error = 0
    init_value = 1023
    kalman = KalmanFilter(p_noise, s_noise, e_error, init_value)
    for data in planarVoltData:
        filteredMeasurement = kalman.getFiltered(data)
        kalman_planarVoltData.append(filteredMeasurement) 
    kalman.meanFix(kalman_planarVoltData)
    #FIXME
    turn = 33
    outerL = 0.034
    inductance = 56e-6
    ramping = input("Ramping Rate of Current : [A/sec]\n")
    ramping = float(ramping)
    # REF
    # SOLDAT
    dBdt = 4.432e-3 * ramping
    indV = inducedV(turn=turn, outerL=outerL, inductance=inductance, dBdt=dBdt)
    print("Induced voltage is %.5E" %(indV))
    print("when Turn = %d, outerL = %f[cm], inductance = %f[uH], dB/dt = %f[T/sec]" %(turn, outerL*100, inductance*math.pow(10,6), dBdt))
    plotdiffScales(timeData, currentData, hallData, "time [sec]", "Current [A]", "Hall Voltage [V]")
    plotScatter(timeData, kalman_planarVoltData, "time [sec]", "Filtered Planar Coil [V]")
    plotScatter(timeData, currentData, "time [Sec]", "current [A]")
    plotScatter(timeData, hallData, "time [Sec]", "Hall Voltage [V]")
    plotScatter(timeData, planarVoltData, "time [Sec]", "Planar Coil [V]")
    plotdiffScales(timeData, kalman_planarVoltData, hallData,'time [sec]', "planar sensor [V]", "Hall data [V]")
    magCalc(tData=timeData, vData=kalman_planarVoltData, turn=turn, outerL=outerL, inductance=inductance)
    plotdiffScales(timeData, calculated_mag, hallData,'time [sec]', "calculated B [T]", "Hall data [V]")    
    
    real_mag = []
    for _idx, item in enumerate(currentData):
        temp = item * 4.432e-3 # [T]
        real_mag.append(temp)

    plotdiffScales(timeData, calculated_mag, real_mag,'time [sec]', "calculated B [T]", "B field [T]")    
    calculated_mag.clear()

    magCalc(tData=timeData, vData=planarVoltData, turn=turn, outerL=outerL, inductance=inductance)
    plotdiffScales(timeData, calculated_mag, hallData,'time [sec]', "calculated B from Raw Data[T]", "Hall data [V]")
    plotdiffScales(timeData, calculated_mag, real_mag,'time [sec]', "calculated B from Raw Data[T]", "B field [T]")
    calculated_mag.clear()
