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
import glob

import struct
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

#if __name__ == '__main__':
#    pg.exec()

    #gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
    # Add a marker
    #gmap.marker(37.770776, -122.461689, 'cornflowerblue')
    # Draw map into HTML file
    #gmap.draw("my_map.html")

def main():
    dir=os.getcwd()
    log_dir = os.path.join(dir,"logs")
    available_events = next(os.walk(log_dir))[1]
    print("Available events: ", available_events)
    event_valid = False
    event_name = input("What event would you like to view? ")  
    event_valid = event_name in available_events     
    while(not event_valid): 
        print("\tEvent:",event_name," invalid")
        event_name = input("What event would you like to view? ")   
        event_valid = event_name in available_events
    print("\t\t Displaying ",event_name)
    G = GUI(event_name)
    G.runGUI()
class GUI:
    def __init__(self, eventName):
        #idk
        self.CWD = os.path.dirname(os.path.realpath(__file__))

        self.eventName = eventName
        self.eventFold = os.path.join(self.CWD,"logs",self.eventName)

        self.LOG_FILE = self.getLastLogPath(self.eventFold) 
        self.Epoc = []

        self.GPS_LAT = []
        self.GPS_LONG = []

        self.CoolantTemp = [];
        self.FuelPressure = [];
        self.OilPressure = [];
        self.OilTemp = [];

        self.AccGraph = None
        self.GyroGraph = None
        self.OilPressureGraph = None
        self.Gauges = None

        self.currentLine = 0;
        return

    def getLastLogPath(self,eventFold):
        files = os.listdir(eventFold)
        paths = [os.path.join(eventFold, basename) for basename in files]
        return max(paths, key=os.path.getctime)
    def updateValuesFromCAN(self):

        def to_int(val, nbits):
            i = int(val, 16)
            if i >= 2 ** (nbits - 1):
                i -= 2 ** nbits
            return i
        #try:
        with open(self.LOG_FILE,'r') as f:
            lines = f.readlines()
            if(len(lines)>self.currentLine+10):
                for i in range(self.currentLine,len(lines)-1):
                    dataLine = lines[i].rstrip();
                    dataLineSplit = dataLine.split("#")
                    arbID = dataLineSplit[0]
                    dataStr = dataLineSplit[1]
                    split = dataStr.split(" ")
                    #print("arbID",arbID,"split",split)
                    
                    if (arbID == "0x3"):
                        GPS_lat_raw = split[3] + split[2]+split[1]+split[0]
                        GPS_long_raw = split[6] + split[5]+split[4]+split[3]

                        GPS_lat = to_int(GPS_lat_raw, 16)/100
                        GPS_long= to_int(GPS_long_raw, 16)/100
                        
                        self.GPS_LAT.append(GPS_lat)
                        self.GPS_LONG.append(GPS_long)
                
                    self.Epoc.append(0)
                print("current line:",self.currentLine,"to:",len(lines))
                self.currentLine = len(lines)
        #except Exception as e:
        #    print(e)
    
    def update(self):
        #global curve, data, ptr, p6
        self.updateValuesFromCAN()
        #self.curve.setData(self.data[self.ptr%10])
        #self.curve.setData(self.Epoc)
        #self.x_curve.setData(self.ACCEL_X)
        #self.y_curve.setData(self.ACCEL_Y)
        #self.z_curve.setData(self.ACCEL_Z)

        
        #self.gx_curve.setData(self.PITCH)
        #self.gy_curve.setData(self.ROLL)
        #self.gz_curve.setData(self.YAW)
        #self.gpsGraph.setData(self.GPS_LAT,self.GPS_LONG)
        self.gpsGraph.plot(self.GPS_LAT,self.GPS_LONG)
        #self.GPS_LONG.append(0.1)
        #self.GPS_LAT.append( 0.1 )
        '''
        if self.ptr == 0:
            self.p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        self.ptr += 1
        '''
        return
    
    def runLayout(self):
        pass
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

        self.gpsGraph = win.addPlot(title="GPS")
        self.gpsGraph.plot(self.GPS_LAT,self.GPS_LONG)


        '''
        p4 = win.addPlot(title="Parametric, grid enabled")
        x = np.cos(np.linspace(0, 2*np.pi, 1000))
        y = np.sin(np.linspace(0, 4*np.pi, 1000))
        p4.plot(x, y)
        '''


        '''
        self.AccGraph = win.addPlot(title="ACCELERATION")
        myRPen=pg.mkPen('r', width=2)
        myBPen=pg.mkPen('b', width=2)
        myGPen=pg.mkPen('g', width=2)
        self.x_curve = self.AccGraph.plot(pen=myRPen, name="X ACCEL")
        #p3 = win.addPl
        self.y_curve = self.AccGraph.plot(pen=myGPen, name="Y ACCEL")
        self.z_curve = self.AccGraph.plot(pen=myBPen, name="Z ACCEL")
        
        '''
        #self.AccGraph.setLimits(xMin=900, xMax=1000, yMin=-20, yMax=20)

        '''
        sub6 = win.addLayout()
        sub6.addLabel("<b>Disable mouse:</b> Per-axis control over mouse input.<br>"
                    "<b>Auto-scale-visible:</b> Automatically fit *visible* data within view<br>"
                    "(try panning left-right).")
        sub6.nextRow()
        v6 = sub6.addViewBox()
        v6.setMouseEnabled(x=True, y=False)
        v6.enableAutoRange(x=False, y=True)
        #v6.setXRange(300, 450)
        v6.setAutoVisible(x=False, y=True)
        l6 = pg.PlotDataItem(y)
        v6.addItem(self.x_curve)
        '''


        '''
        win.nextRow()

        p3 = win.addPlot(title="EULER")
        self.gx_curve = p3.plot(pen=myRPen,name="PITCH")
        self.gy_curve = p3.plot(pen=myGPen,name="ROLL")
        self.gz_curve = p3.plot(pen=myBPen,name="YAW")
        '''
        #self.gz_curve = p3.plot(pen=(0,0,0),name="YAW")
        #p3.setLimits(xMin=0, xMax=.5, yMin=0, yMax=400)




         
        #self.data = np.random.normal(size=(10,1000))
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