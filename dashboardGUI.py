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
        return
    def boycott(self):
        try:
            with open(self.LOG_FILE, 'r') as f:
                last_line = f.readlines()[-1]
                #print(last_line)
                remFrame = last_line.split("=>")

                split = remFrame[1].split(" ");
                #print(split)
                self.Epoc.append(2*float(split[-2]))
                print(self.Epoc)
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
        self.boycott()
        #self.curve.setData(self.data[self.ptr%10])
        self.curve.setData(self.Epoc)
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
        x = np.cos(np.linspace(0, 2*np.pi, 1000))
        y = np.sin(np.linspace(0, 4*np.pi, 1000))
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