"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

import numpy as np
import os
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from gmplot import gmplot
import ctypes
import numpy

import struct

#if __name__ == '__main__':
#    pg.exec()

    #gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
    # Add a marker
    #gmap.marker(37.770776, -122.461689, 'cornflowerblue')
    # Draw map into HTML file
    #gmap.draw("my_map.html")

def main():
    dir=os.getcwd()
    G = GUI()
    G.runGUI()
class GUI:
    def __init__(self):
        #idk
        self.CWD = os.path.dirname(os.path.realpath(__file__))
        self.LOG_FILE = os.path.join(self.CWD, "log.txt")
        self.Epoc = []
        self.ACCEL_X = []
        self.ACCEL_Y = []
        self.ACCEL_Z = []

        self.PITCH = []
        self.ROLL = []
        self.YAW = []

        self.currentLine = 0;


        return
    

    def updateValuesFromCAN(self):

        def to_int(val, nbits):
            i = int(val, 16)
            if i >= 2 ** (nbits - 1):
                i -= 2 ** nbits
            return i
        try:
            with open(self.LOG_FILE, 'r') as f:
                last_line = f.readlines()[-1]
                #print(last_line)
                remFrame = last_line.split("=>")

                split = remFrame[1].strip().split(" ");
                #print(split)
                if("0x121" in split[0] ):
                    # this is acceleration
                    ax_raw = split[2]+split[1]
                    ay_raw = split[4]+split[3]
                    az_raw = split[6]+split[5]
                    #print(split[2],split[1],"makes")
                    #acc_dx = float.fromhex(ax_raw)/100
                    acc_dx = to_int(ax_raw, 16)/100
                    #acc_dy = float.fromhex(ay_raw)/100
                    acc_dy = to_int(ay_raw, 16)/100
                    #acc_dz = float.fromhex(az_raw)/100
                    acc_dz = to_int(az_raw, 16)/100
                    self.ACCEL_X.append(acc_dx)
                    self.ACCEL_Y.append(acc_dy)
                    self.ACCEL_Z.append(acc_dz)
                    
                    print(split,"RAW:FL",ax_raw,":",acc_dx,ay_raw,":",acc_dy,az_raw,":",acc_dz)
                elif("0x132" in split[0]):
                    gx_raw = split[2]+split[1]
                    gy_raw = split[4]+split[3]
                    gz_raw = split[6]+split[5]
                    gyr_dx = to_int(gx_raw, 16)/100
                    gyr_dy = to_int(gy_raw, 16)/100
                    gyr_dz = to_int(gz_raw, 16)/100
                    self.PITCH.append(gyr_dx)
                    self.ROLL.append(gyr_dy)
                    self.YAW.append(gyr_dz)
                    print(split,"RAW:FL",gx_raw,":",gyr_dx,gy_raw,":",gyr_dy,gz_raw,":",gyr_dz)
                else:
                    print("Nothing")

                
                self.Epoc.append(2*float(split[-1]))
                
                #flt = struct.unpack('!f', bytes.fromhex('41973333'))[0]
                #print(self.Epoc)
                '''
                self.global_head_temperature = abs(round(float(split[0]),1))
                self.global_coolant_temperature = abs(round(float(split[1]),1))
                self.global_fuel_pressure = abs(round(float(split[2]),1))
                
                self.global_speed = abs(round(float(split[2]),1))
                self.global_rpm = (abs(round(float(split[2]),1))/200) * 5600  
                '''
        except Exception as e:
            print(e)
    
    def update(self):
        #global curve, data, ptr, p6
        self.updateValuesFromCAN()
        #self.curve.setData(self.data[self.ptr%10])
        self.curve.setData(self.Epoc)
        self.x_curve.setData(self.ACCEL_X)
        self.y_curve.setData(self.ACCEL_Y)
        self.z_curve.setData(self.ACCEL_Z)

        
        self.gx_curve.setData(self.PITCH)
        self.gy_curve.setData(self.ROLL)
        self.gz_curve.setData(self.YAW)

        if self.ptr == 0:
            self.p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        self.ptr += 1
        return
    
    def runGUI(self):
        app = pg.mkQApp("Plotting Example")
        #mw = QtWidgets.QMainWindow()
        #mw.resize(800,800)

        win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        win.resize(1000,600)
        win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        #p4 = win.addPlot(title="Parametric, grid enabled")
        #x = np.cos(np.linspace(0, 2*np.pi, 1000))
        #y = np.sin(np.linspace(0, 4*np.pi, 1000))
        #p4.plot(x, y)
        #p4.showGrid(x=True, y=True)

        #p5 = win.addPlot(title="Scatter plot, axis labels, log scale")
        x = np.random.normal(size=1000) * 1e-5
        y = x*1000 + 0.005 * np.random.normal(size=1000)
        y -= y.min()-1.0
        mask = x > 1e-15
        x = x[mask]
        y = y[mask]
        #p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
        #p5.setLabel('left', "Y Axis", units='A')
        #p5.setLabel('bottom', "Y Axis", units='s')
        #p5.setLogMode(x=True, y=False)
        p2 = win.addPlot(title="ACCELERATION")
        self.x_curve = p2.plot(pen=(255,0,0), name="X ACCEL")
        #p3 = win.addPl
        self.y_curve = p2.plot(pen=(0,255,0), name="Y ACCEL")
        self.z_curve = p2.plot(pen=(0,0,255), name="Z ACCEL")

        p3 = win.addPlot(title="EULER")
        self.gx_curve = p3.plot(pen=(255,0,0),name="PITCH")
        self.gy_curve = p3.plot(pen=(0,255,0),name="ROLL")
        self.gz_curve = p3.plot(pen=(0,0,255),name="YAW")


        self.p6 = win.addPlot(title="Updating plot")
        self.curve = self.p6.plot(pen='y')



        self.data = np.random.normal(size=(10,1000))
        self.ptr = 0
        
        '''
        def update():
            #global curve, data, ptr, p6
            
            self.curve.setData(self.data[self.ptr%10])
            if self.ptr == 0:
                p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            self.ptr += 1
        '''
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(50)

        pg.exec()

        

main()