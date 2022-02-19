# Software for visualization of RTStruct structures on CT images

Project made for the course - Information Technology Systems in Medicine

![visualization of RTStruct structures on CT images](https://github.com/Adam1904/Software-for-visualization-of-RTStruct-structures-on-CT-images/blob/main/gui.png)

## Design

This script is responsible for the operation of the program, it is responsible for both creating the GUI and the 
process of processing images from dicom files. The program is based on the use of the PyQt5 library, on the basis 
of which the entire interface containing the appropriate buttons and functions was created.

The operation of the program is based on the visualization of CT structures that can be changed using the mouse 
buttons. Accordingly, the scroll function changes the imaging cross-sections, while after pressing the left button 
and moving the mouse, we are able to change the window windth and window center of ct scan. Pressing "+", or "-" on 
the keyboard, is responsible for changing the selected contour from the RT Structure file. The intuitive GUI allows 
you to easily display linked images.

The operation of GUI is based on the creation of methods that respond appropriately to the user's commands. 
The two main buttons are responsible for uploading the necessary dicom files to the programs. The program is able 
to check if a given file has the appropriate extension, so selecting the wrong folder will not interrupt the program.

## Dependiencies

This script requires following libraries to be installed: 
- PyQt5 - PyQt5 is a comprehensive set of Python bindings for Qt v5, implemented as more than 35 extension modules, 
    enables Python to be used as an alternative application development language to C++ on all supported platforms
- matplotlib - comprehensive plotting library for creating static, animated and interactive visualizations in Python 
    programing language and its numerical mathematics extension NumPy,
- dicom_csv - collection of utils for gathering, aggregation and handling metadata from DICOM files, includes 
    functions for gathering metadata from individual DICOM files or entire directories and tools for grouping DICOM 
    metadata into images, 
- numpy - library for scientific computing with Python programing language, including support for multi-dimensional 
    arrays and matrices and functions to operate on them, 
- sys - a module that provides access to some variables used or maintained by the interpreter and to functions that 
    interact strongly with the interpreter, provides various functions and variables that are used to manipulate 
    different parts of the Python runtime environment
- cv2 - opencv-python library, an open-source library that includes several hundreds of computer vision algorithms
- pydicom - pure Python package for working with DICOM files, which allows user to read complex files into pythonic 
    structures for manipulation, save the modified datasets as DICOM format files
- os - a Python module which provides a portable way of using operating system dependent functionality, it comes under
     Python's standard utility modules
## Prerequisites

```sh
> pip install numpy
> pip install pydicom
> pip install opencv-python
> pip install matplotlib
> pip install dicom-csv
```

## Execution
To run the code, type:

```
python3 app.py
```

## Things to improve in the future

- more precise centering of RTStruct structures
