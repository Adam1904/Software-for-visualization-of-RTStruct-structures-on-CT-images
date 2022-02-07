"""

Software for visualization of RTStruct structures on CT images

This script is responsible for the operation of the program, it is responsible for both creating the GUI and the 
process of processing images from dicom files. The program is based on the use of the PyQt5 library, on the basis 
of which the entire interface containing the appropriate buttons and functions was created.

The operation of the program is based on the visualization of CT structures that can be changed using the mouse 
buttons. Accordingly, the scroll function changes the imaging cross-sections, while after pressing the left button 
and moving the mouse, we are able to change the window windth and window center of ct scan. Pressing "+", or "-" on 
the keyboard, is responsible for changing the selected contour from the RT Structure file. The intuitive GUI allows 
you to easily display linked images.

The operation of gui is based on the creation of methods that respond appropriately to the user's commands. 
The two main buttons are responsible for uploading the necessary dicom files to the programs. The program is able 
to check if a given file has the appropriate extension, so selecting the wrong folder will not interrupt the program.

This script requires following libraries to be installed: 
 • PyQt5 - PyQt5 is a comprehensive set of Python bindings for Qt v5, implemented as more than 35 extension modules, 
    enables Python to be used as an alternative application development language to C++ on all supported platforms
 • matplotlib - comprehensive plotting library for creating static, animated and interactive visualizations in Python 
    programing language and its numerical mathematics extension NumPy,
 • dicom_csv - collection of utils for gathering, aggregation and handling metadata from DICOM files, includes 
    functions for gathering metadata from individual DICOM files or entire directories and tools for grouping DICOM 
    metadata into images, 
 • numpy - library for scientific computing with Python programing language, including support for multi-dimensional 
    arrays and matrices and functions to operate on them, 
 • sys - a module that provides access to some variables used or maintained by the interpreter and to functions that 
    interact strongly with the interpreter, provides various functions and variables that are used to manipulate 
    different parts of the Python runtime environment
 • cv2 - opencv-python library, an open-source library that includes several hundreds of computer vision algorithms
 • pydicom - pure Python package for working with DICOM files, which allows user to read complex files into pythonic 
    structures for manipulation, save the modified datasets as DICOM format files
 • os - a Python module which provides a portable way of using operating system dependent functionality, it comes under
     Python's standard utility modules

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from dicom_csv import *
import numpy as np
import sys
import cv2
import pydicom as dicom
import os

class MainWindow(QtWidgets.QMainWindow):
    """
    A class responsible for creating the main gui window. It inherits from the class QMainWindow from PyQt5.QtWidgets 
    module. The central QtWidget contains two QPushButton objects, the first QPushButton object is responsible for 
    allowing the user to open the folder containing the DICOM format files, the second QPushButton object is responsible 
    for allowing the user to open the RTStruct file in DICOM format. The QtWidget contains four QLabel objects, which 
    display the information about the window center, the window width, the section number and the number of displayed 
    structure. The QtWidget contains also QGraphicsView, which is responsible for displaying the images in the main 
    application window. 

    Attributes
    ----------
    lastXPos : int 
        auxiliary variable, needed to calculate the mouse position (last position in the x axis)
    lastYPos : int 
        auxiliary variable, needed to calculate the mouse position (last position in the y axis)
    lastRollPos : int 
        variable responsible for storing the last value of the scroll button
    wc : int
        variable responsible for calculating the window center based on the mouse movement
    ww : int
        variable responsible for calculating the window width based on the mouse movement
    currentWW : int
        the variable responsible for the currently set window width value
    currentWC : int
        the variable responsible for the currently set window center value
    currentRollPos : int
        the variable responsible for the currently set slice of CT scans
    numOfSlice : int
        variable responsible for the section number
    ctset : array containing str
        variable holding a set of CT scan
    rtstruct : FileDataset
        variable holding the RTStruct file
    rtstructpath : str
        variable responsible for the path to the RTStruct file
    pixelSpacing : int
        variable responsible for the distance between pixels
    numOfRTStruct : int
        variable responsible for displayed structure
    RTStructColour : RGB triplet color representation [e.g. (255,0,0)]
        variable storing thr colour of dsplayed structure

    Methods
    -------
    __init__()
        the method responsible for creation
    
    wheelEvent(event: QtGui.QWheelEvent)
        the method responsible for the appropriate reaction to the movement of the mouse scroll (up/down movement)

    mouseMoveEvent(event: QtGui.QWheelEvent)
        the method responsible for the correct reaction to the mouse movement(collects information about the movement of the mouse)

    mousePressEvent(event: QtGui.QWheelEvent)
        the method that checks if the user pressed the mouse button

    mouseReleaseEvent(event: QtGui.QWheelEvent)
        the method that checks if the user has released the mouse button

    loadImage(number)
        the method responsible for reading the appropriate CT slice with the number "number"

    pushButton_handler()
        the handler which is listening if the user pressed the first button in the main menu (responsible for loading CT scan files in dicom format)

    pushButton_handler2()
        the handler which is listening if the user pressed the second button in the main menu (responsible for loading RTStruct file in dicom format)

    loadRT()
        the method responsible for reading the structures that were previously retrieved from the file

    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing

        """
        super(MainWindow, self).__init__()
        """ creating and assigning individual elements of gui """
        screen = QDesktopWidget().screenGeometry()
        self.setWindowTitle("Software for visualization of RTStruct structures on CT images")
        self.centralWidget = QtWidgets.QWidget(self)
        self.resize((int)(screen.width()*70/100),(int)(screen.height()*80/100)) # size of window 1300x900
        self.setFixedSize(self.size()) # setting a fixed size of the main window
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropFrame = QtWidgets.QFrame(self.centralWidget)
        self.dropFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropFrame.setObjectName("dropFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dropFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.dropFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.dropFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(80)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(130, 80))
        self.pushButton.setObjectName("buttonDICOM")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 4, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.dropFrame)
        self.setCentralWidget(self.centralWidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.dropFrame)
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(130, 80))
        self.pushButton_2.setObjectName("buttonRTStruct")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 4, 1)
        self.label = QtWidgets.QLabel(self.dropFrame)
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(130, 20))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 2, 1, 1)
        self.label2 = QtWidgets.QLabel(self.dropFrame)
        self.label2.setSizePolicy(sizePolicy)
        self.label2.setMinimumSize(QtCore.QSize(130, 20))
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 2, 2, 1, 1)
        self.label3 = QtWidgets.QLabel(self.dropFrame)
        self.label3.setSizePolicy(sizePolicy)
        self.label3.setMinimumSize(QtCore.QSize(130, 20))
        self.label3.setObjectName("label3")
        self.gridLayout.addWidget(self.label3, 3, 2, 1, 1)
        self.label4 = QtWidgets.QLabel(self.dropFrame)
        self.label4.setSizePolicy(sizePolicy)
        self.label4.setMinimumSize(QtCore.QSize(130, 20))
        self.label4.setObjectName("label4")
        self.gridLayout.addWidget(self.label4, 4, 2, 1, 1)

        """ renaming individual gui elements """
        _translate = QtCore.QCoreApplication.translate 
        self.pushButton.setText(_translate("SplashScreen", "Open DICOM folder"))
        self.pushButton.clicked.connect(self.pushButton_handler) # setting the push button (Open DICOM folder) handler
        self.pushButton_2.setText(_translate("SplashScreen", "Open RTStruct file"))
        self.pushButton_2.clicked.connect(self.pushButton_handler2) # setting the push button (Open RTStruct file) handler
        self.label.setText(_translate("SplashScreen", "Window width: 1000"))
        self.label2.setText(_translate("SplashScreen", "Window center: 1000"))
        self.label3.setText(_translate("SplashScreen", "Number of slice: 0"))
        self.label4.setText(_translate("SplashScreen", "Number of contour: 0"))
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        """ setting rules and handlers """
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # disable of scroll bars
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setCursor(QtCore.Qt.CrossCursor) # setting a custom cursor
        self.graphicsView.setMouseTracking(True) # setting a policy that watches over mouse movements
        self.graphicsView.mouseMoveEvent = self.mouseMoveEvent # setting the mouse move event handler
        self.graphicsView.mouseReleaseEvent = self.mouseReleaseEvent # setting the mouse release event handler
        self.graphicsView.mousePressEvent = self.mousePressEvent # setting the mouse press event handler
        self.graphicsView.keyPressEvent = self.keyPressEvent # setting the key press event handler

        """ creating global variables """
        self.lastXPos = 0 # auxiliary variable, needed to calculate the mouse position (last position in the x axis)
        self.lastYPos = 0 # auxiliary variable, needed to calculate the mouse position (last position in the y axis)
        self.lastRollPos = 0 # variable responsible for storing the last value of the scroll button
        self.wc = 1000 # variable responsible for calculating the window center based on the mouse movement
        self.ww = 1000 # variable responsible for calculating the window width based on the mouse movement
        self.currentWW = self.ww # the variable responsible for the currently set window width value
        self.currentWC = self.wc # the variable responsible for the currently set window center value
        self.currentRollPos = 0 # the variable responsible for the currently set slice of CT scans
        self.numOfSlice = 0 # variable responsible for the section number
        self.ctset = None # variable holding a set of CT scan
        self.rtstruct = None # variable holding the RTStruct file
        self.rtstructpath = None # variable responsible for the path to the RTStruct file
        self.pixelSpacing = None # variable responsible for the distance between pixels
        self.numOfRTStruct = 0 # variable responsible for displayed structure
        self.RTStructColour = None # variable storing the colour of dsplayed structure
        self.patientCenterPos = [0,0] # variable storing point of the patient's center

    def wheelEvent(self, event: QtGui.QWheelEvent):
        """
        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event. 

        Returns
        -------
        Nothing

        """
        if self.ctset is not None:  # checking that the collection is not empty
            maxSize = len(self.ctset)
            # proper handling of the scroll button
            if event.angleDelta().y() > 0 :
                if self.lastRollPos < maxSize:
                    self.lastRollPos += 1 # if we scroll up (icrementation)
                if self.lastRollPos < maxSize: # keeping an eye on whether or not we have gone beyond the number of available slices
                    pass
            elif event.angleDelta().y() < 0:
                if self.lastRollPos > 0:
                    self.lastRollPos -= 1  # if we scroll down (decrementation)
            
            if self.ctset is not None:
                if self.currentRollPos != self.lastRollPos: # change the current position if it is different
                    self.currentRollPos = self.lastRollPos 
                    self.loadImage(self.lastRollPos) # reloading the image

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """
        Parameters
        ----------
        event : QtGui.QKeyEvent
            The QWheelEvent class contains parameters that describes a key event
        
        Returns
        -------
        Nothing

        """
        if event.text() == "+": # if the '+' button was pressed, change structure forward
            if self.rtstructpath is not None:
                if self.numOfRTStruct == (len(self.rtstruct.ROIContourSequence)-1): # checking whether the maximum number of slices has not been exceeded
                    self.numOfRTStruct = 0
                else:
                    self.numOfRTStruct += 1 # slice incrementation
                self.label4.setText("Number of contour: " + str(self.numOfRTStruct) + "/" + str(len(self.rtstruct.ROIContourSequence)-1))
                self.loadRT() # reloading the image
        if event.text() == "-": # if the '-' button was pressed, change structure backwards
            if self.rtstructpath is not None:
                if self.numOfRTStruct == 0: # checking whether the maximum number of slices has not been exceeded
                    self.numOfRTStruct = (len(self.rtstruct.ROIContourSequence)-1)
                else:
                    self.numOfRTStruct -= 1 # slice decrementation
                self.label4.setText("Number of contour: " + str(self.numOfRTStruct) + "/" + str(len(self.rtstruct.ROIContourSequence)-1))
                self.loadRT() # reloading the image   
    
    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """
        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event. 
        
        Returns
        -------
        Nothing

        """
        if event.buttons() == QtCore.Qt.LeftButton: # detection if the left mouse button has been pressed
            self.wc += (int)((event.x() - self.lastXPos)/ 100) # setting the appropriate value window center
            self.ww += (int)((event.y() - self.lastYPos)/ 100) # setting the appropriate value window width
            
            # checking whether the adopted threshold is not exceeded (if so, then setting the maximum values)
            if self.wc > 3095:
                self.wc = 3095 # maximum value of window center
            
            if self.wc < -1024:
                self.wc = -1024 # maximum value of window center
            
            if self.ww > 4096:
                self.ww = 4096 # maximum value of window width
            
            if self.ww < 1:
                self.ww = 1 # maximum value of window width
            
            self.label.setText( "Window width: " + str(self.ww))
            self.label2.setText( "Window center: " + str(self.wc))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """
        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event. 
        
        Returns
        -------
        Nothing

        """
        self.lastXPos = event.x() # save the last position of the mouse
        self.lastYPos = event.y()
            
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """
        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event. 
        
        Returns
        -------
        Nothing

        """
        self.lastXPos = None # set the variables to None when you release the mouse
        self.lastYPos = None
        if self.ctset is not None and self.image is not None: 
            if self.currentWW != self.ww or self.currentWC != self.wc: # checking if the window width, and window center values have changed
                    self.currentWW = self.ww # changing window width
                    self.currentWC = self.wc # changing window center
                    #print("WW: " + str(self.currentWC) + ", WC: " + str(self.currentWW))
                    self.loadImage(self.numOfSlice) # reloading the image

    def loadImage(self, number):
        """
        Parameters
        ----------
        number : int
            The slice number of the ct scan that is currently displayed
        
        Returns
        -------
        Nothing

        """
        try:
            if number >= 0 and number < len(self.ctset):
                self.numOfSlice = number # setting the slice number
                self.label3.setText("Number of slice: " + str(self.numOfSlice) + "/" + str(len(self.ctset)))
                dataset = dicom.dcmread(self.ctset[number],force=True) # reading dicom file with dcmread() method
                
                self.data = dataset.pixel_array # extraction of a pixel array
                self.image = cv2.resize(self.data,None, fx = 3, fy = 3, interpolation = cv2.INTER_LINEAR) # appropriate interpolation        
                # setting chosen window width and window center 
                self.image = np.clip(self.image - (self.currentWC - self.currentWW/2),0,self.currentWW-1) * 256/self.currentWW 
                self.image = cv2.cvtColor(self.image.astype(np.uint8),cv2.COLOR_GRAY2BGR) # switch to grayscale

                if self.rtstruct is not None and len(self.planesArray) != 0 and self.flag: # The flag ensures correct loading of RTStruct files
                    w,h = self.image.shape[:2] # getting resolution of displayed image
                    resolution = dataset.Rows * dataset.Columns
                    X_center = (int)(abs(self.patientCenterPos[0]*w*h/resolution))  # establishing the center of the patient in the image
                    Y_center = (int)(abs(self.patientCenterPos[1]*w*h/resolution)) 
                    if len(self.planesArray) >= len(self.ctset): # checking whether the slices limit has not been exceeded
                        for i in range(0,len(self.planesArray[self.numOfSlice][0])):
                            # the distribution of the points depends on the number of rows and columns of the ct scan display
                            if self.planesArray[self.numOfSlice][0][i] != None:
                                elementx = (int)(self.planesArray[self.numOfSlice][0][i]*w*h/resolution) # rescaling the points of structures
                            if self.planesArray[self.numOfSlice][1][i] != None:
                                elementy = (int)(self.planesArray[self.numOfSlice][1][i]*w*h/resolution) 
                            # adding RTStruct structures to the image inside try - except block 
                            try:
                                self.image = cv2.circle(self.image, ((elementx+X_center),(elementy+Y_center)), radius=0, color=self.RTStructColour, thickness=8)
                            except:
                                self.image = cv2.circle(self.image, ((elementx+X_center),(elementy+Y_center)), radius=0, color=(255,0,0), thickness=8)
 
                # creating an image from data (using the Format_RGB888 format)
                self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], QImage.Format_RGB888)
                self.pixmap = QPixmap.fromImage(self.image) # create a pixmap from a modified image
                self.scene.addPixmap(self.pixmap.scaled(self.graphicsView.width()-2,self.graphicsView.height()-2)) # scaling the pixmap to the size of the widget
                self.graphicsView.setScene(self.scene) # setting scene
                self.graphicsView.show()
        except Exception as e:
            print("An unexpected exception occured: " + str(e))    
                
    def pushButton_handler(self):
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing

        """
        try:
            path = QFileDialog.getExistingDirectory() # selecting the folder containing the ct files
            self.ctpath = path
                
            if os.path.isdir(self.ctpath):
                self.scene = QGraphicsScene()
                # find all files in the selected folder
                self.ctset = [os.path.join(self.ctpath,f) for f in os.listdir(self.ctpath) if os.path.isfile(os.path.join(self.ctpath, f))]
                ctimages = []
            
                counterCT = 0 
                if self.ctset is not None:
                    for f in self.ctset:
                        if f[-3:] == "dcm": # checking if the file has the 'dcm' extension
                            ct = dicom.dcmread(f, force=True) # reading ct scans from dicom file 
                            if 'PixelData' in ct:
                                ctimages.append((f,ct.ImagePositionPatient)) # insertion of the ct file associated with the patient's position
                                self.patientCenterPos[0] = ct.ImagePositionPatient[0]
                                self.patientCenterPos[1] = ct.ImagePositionPatient[1]
                                counterCT += 1
                    if counterCT == len(self.ctset): # checking whether the slices limit has not been exceeded
                        ctimages.sort(key=lambda x:x[1][2]) # sorting ct scans by patient's position
                        if len(self.ctset) > 0:
                            self.loadImage(0) # reloading the image
            self.label3.setText("Number of slice: " + str(self.numOfSlice) + "/" + str(len(self.ctset)))
        except Exception as e:
            print("An unexpected exception occured: " + str(e))
    
    def pushButton_handler2(self):
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing

        """
        try:
            self.rtstructpath = QFileDialog.getOpenFileName() # select the file (must be dicom format)
            self.rtstructpath = self.rtstructpath[0]
            if ".dcm" in self.rtstructpath: # checking if the file has the 'dcm' extension
                self.rtstruct = dicom.dcmread(self.rtstructpath, force=True) # reading RTStruct structures from dicom file
                if 'ROIContourSequence' in self.rtstruct:
                    self.loadRT() # reloading the image
                else:
                    self.rtstruct = None
            self.label4.setText("Number of contour: " + str(self.numOfRTStruct) + "/" + str(len(self.rtstruct.ROIContourSequence)-1))
        except Exception as e:
            print("An unexpected exception occured: " + str(e))

    def loadRT(self):    
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing     

        """
        if self.rtstructpath is not None:
                self.planes = None 
                self.flag = True # The flag ensures correct loading of RTStruct files
                if 'ROIContourSequence' in self.rtstruct: # checking if it is a file containing RTStruct structures
                    try:
                        sequences = self.rtstruct.ROIContourSequence[self.numOfRTStruct].ContourSequence # saving sequence of structures
                        self.RTStructColour = self.rtstruct.ROIContourSequence[self.numOfRTStruct].ROIDisplayColor # recovering the color of the structure
                    except:
                        print("There were problems with getting structures from Structure file")
                        self.flag = False

                    try:
                        if sequences is not None and self.flag:
                            self.planes = {} # dictionary of sections
                            for c in sequences:
                                array = [c.ContourData[i:i+3] for i in range(0, len(c.ContourData), 3)] # appropriate reading of the pixel positions of the structures

                                z = str(round(array[0][2], 2)) # rounding of the z element
                            
                                if z not in self.planes:
                                    self.planes[z] = [] 
                                self.planes[z].append(array) # saving array by (patient's position)
                    except UnboundLocalError:
                        print("The local variable 'sequences' referenced before assignment")
                    except Exception as e:
                        print("An unexpected exception occured: " + str(e))
                
                try:
                    if self.planes is not None and self.flag:
                        self.planesArray = [[None for y in range(2)] for x in range(len(self.planes))] # array preallocation
        
                        counterofslices = 0
                    
                        for i in self.planes: 
                            xpoints = []
                            ypoints = []
                            for c in self.planes.get(i)[0]: # iterating over all slices for a given structure
                                xpoints.append(c[0]) # add x points to list
                                ypoints.append(c[1]) # add y points to list
                            self.planesArray[counterofslices][0] = xpoints # saving the position (x, y) of points that make up the structures in the table
                            self.planesArray[counterofslices][1] = ypoints
                            counterofslices += 1

                        self.planesArray = self.planesArray[::-1] # reverse the data so that they can be displayed correctly
                        self.planes = None 
        
                        if self.ctset is not None:
                            self.loadImage(self.currentRollPos) # reloading the image
                    
                except Exception as e:
                    print("An unexpected exception occured: " + str(e))
           
""" The main function """
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    mainWindow = MainWindow() # main window of the graphical user interface
    mainWindow.show() # calling method show() which shows the main window
    sys.exit(app.exec())