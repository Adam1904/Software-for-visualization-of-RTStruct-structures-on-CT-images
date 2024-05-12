"""

Software for visualization of RTStruct structures on CT images

This script is responsible for the operation of the program, it is responsible for both creating the GUI and the
process of processing images from dicom files. The program is based on the use of the PyQt5 library, on the basis
of which the entire interface containing the appropriate buttons and functions was created.

The operation of the program is based on the visualization of CT structures that can be changed using the mouse
buttons. Accordingly, the scroll function changes the imaging cross-sections, while after pressing the left button
and moving the mouse, we are able to change the window width and window center of ct scan. The intuitive GUI allows
you to easily display linked images.

The operation of gui is based on the creation of methods that respond appropriately to the user's commands.
The two main buttons are responsible for uploading the necessary dicom files to the programs. The program is able
to check if a given file has the appropriate extension, so selecting the wrong folder will not interrupt the program.

This script requires following libraries to be installed:
 • PyQt5 - PyQt5 is a comprehensive set of Python bindings for Qt v5, implemented as more than 35 extension modules,
    enables Python to be used as an alternative application development language to C++ on all supported platforms
 • matplotlib - comprehensive plotting library for creating static, animated and interactive visualizations in Python
    programming language and its numerical mathematics extension NumPy,
 • dicom_csv - collection of utils for gathering, aggregation and handling metadata from DICOM files, includes
    functions for gathering metadata from individual DICOM files or entire directories and tools for grouping DICOM
    metadata into images,
 • numpy - library for scientific computing with Python programming language, including support for multi-dimensional
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
from utils import *
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
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setWindowTitle(
            "Software for visualization of RTStruct structures on CT images"
        )
        self.central_widget = QtWidgets.QWidget(self)
        self.window_center_position = (
            (int)(screen.width() * 70 / 100 / 2),
            (int)(screen.height() * 80 / 100 / 2),
        )
        self.resize(
            (int)(screen.width() * 70 / 100), (int)(screen.height() * 80 / 100)
        )  # set fixed size of window 1300x900
        self.setFixedSize(self.size())  # setting a fixed size of the main window
        self.central_widget.setObjectName("central_widget")
        self.vertical_layout_up = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout_up.setObjectName("vertical_layout_up")
        self.drop_frame = QtWidgets.QFrame(self.central_widget)
        self.drop_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.drop_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.drop_frame.setObjectName("drop_frame")
        self.vertical_layout_down = QtWidgets.QVBoxLayout(self.drop_frame)
        self.vertical_layout_down.setObjectName("vertical_layout_down")
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.graphics_view = QtWidgets.QGraphicsView(self.drop_frame)
        self.graphics_view.setObjectName("graphics_view")
        self.grid_layout.addWidget(self.graphics_view, 0, 0, 1, 3)
        self.push_button_dicom = QtWidgets.QPushButton(self.drop_frame)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(80)
        size_policy.setHeightForWidth(
            self.push_button_dicom.sizePolicy().hasHeightForWidth()
        )
        self.push_button_dicom.setSizePolicy(size_policy)
        self.push_button_dicom.setMinimumSize(QtCore.QSize(130, 80))
        self.push_button_dicom.setObjectName("push_button_dicom")
        self.grid_layout.addWidget(self.push_button_dicom, 1, 0, 4, 1)
        self.vertical_layout_down.addLayout(self.grid_layout)
        self.vertical_layout_up.addWidget(self.drop_frame)
        self.setCentralWidget(self.central_widget)
        self.push_button_rt = QtWidgets.QPushButton(self.drop_frame)
        self.push_button_rt.setSizePolicy(size_policy)
        self.push_button_rt.setMinimumSize(QtCore.QSize(130, 80))
        self.push_button_rt.setObjectName("push_button_rt")
        self.grid_layout.addWidget(self.push_button_rt, 1, 1, 4, 1)

        self.label_window_width = QtWidgets.QLabel(self.drop_frame)
        self.label_window_width.setSizePolicy(size_policy)
        self.label_window_width.setMinimumSize(QtCore.QSize(130, 20))
        self.label_window_width.setObjectName("label_window_width")
        self.grid_layout.addWidget(self.label_window_width, 1, 2, 1, 1)
        self.label_window_center = QtWidgets.QLabel(self.drop_frame)
        self.label_window_center.setSizePolicy(size_policy)
        self.label_window_center.setMinimumSize(QtCore.QSize(130, 20))
        self.label_window_center.setObjectName("label_window_center")
        self.grid_layout.addWidget(self.label_window_center, 2, 2, 1, 1)
        self.label_slice_number = QtWidgets.QLabel(self.drop_frame)
        self.label_slice_number.setSizePolicy(size_policy)
        self.label_slice_number.setMinimumSize(QtCore.QSize(130, 20))
        self.label_slice_number.setObjectName("label_slice_number")
        self.grid_layout.addWidget(self.label_slice_number, 3, 2, 1, 1)
        self.label_blank_space = QtWidgets.QLabel(self.drop_frame)
        self.label_blank_space.setSizePolicy(size_policy)
        self.label_blank_space.setMinimumSize(QtCore.QSize(130, 20))
        self.label_blank_space.setObjectName("label_blank_space")
        self.grid_layout.addWidget(self.label_blank_space, 4, 2, 1, 1)

        self.create_menu_bar()

        """ renaming individual gui elements """
        _translate = QtCore.QCoreApplication.translate
        self.push_button_dicom.setText(_translate("SplashScreen", "Open DICOM folder"))
        self.push_button_dicom.clicked.connect(
            self.push_button_dicom_dir
        )  # setting the push button (Open DICOM folder) handler
        self.push_button_rt.setText(_translate("SplashScreen", "Open RTStruct file"))
        self.push_button_rt.clicked.connect(
            self.push_button_rtstruct_file
        )  # setting the push button (Open RTStruct file) handler
        self.label_window_width.setText(
            _translate("SplashScreen", "Window width: 1000")
        )
        self.label_window_width.setFont(QtGui.QFont("Arial", 20))
        self.label_window_center.setText(
            _translate("SplashScreen", "Window center: 1000")
        )
        self.label_window_center.setFont(QtGui.QFont("Arial", 20))
        self.label_slice_number.setText(
            _translate("SplashScreen", "Number of slice: 0")
        )
        self.label_slice_number.setFont(QtGui.QFont("Arial", 20))
        self.label_window_width.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.label_window_center.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.label_slice_number.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.label_blank_space.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )

        """ setting rules and handlers """
        self.graphics_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )  # disable of scroll bars
        self.graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setCursor(QtCore.Qt.CrossCursor)  # setting a custom cursor
        self.graphics_view.setMouseTracking(
            True
        )  # setting a policy that watches over mouse movements
        self.graphics_view.mouseMoveEvent = (
            self.mouse_move_event
        )  # setting the mouse move event handler
        self.graphics_view.mouseReleaseEvent = (
            self.mouse_release_event
        )  # setting the mouse release event handler
        self.graphics_view.mousePressEvent = (
            self.mouse_press_event
        )  # setting the mouse press event handler

        """ creating global variables """
        self.last_x_position = 0  # auxiliary variable, needed to calculate the mouse position (last position in the x axis)
        self.last_y_position = 0  # auxiliary variable, needed to calculate the mouse position (last position in the y axis)
        self.last_rolled_position = (
            0  # variable responsible for storing the last value of the scroll button
        )
        self.window_center = 1000  # variable responsible for calculating the window center based on the mouse movement
        self.window_width = 1000  # variable responsible for calculating the window width based on the mouse movement
        self.current_window_width = (
            self.window_width
        )  # the variable responsible for the currently set window width value
        self.current_window_center = (
            self.window_center
        )  # the variable responsible for the currently set window center value
        self.current_rolled_position = (
            0  # the variable responsible for the currently set slice of CT scans
        )
        self.current_slice = 0  # variable responsible for the section number
        self.merged_images = None
        self.rt_structures = None
        self.rt_struct_color = (255, 0, 0)
        self.path_to_ct_dir = None
        self.path_to_rt_file = (
            None  # variable responsible for the path to the RTStruct file
        )
        self.scene = QtWidgets.QGraphicsScene()

    def set_loading_screen(self) -> None:
        """
        Function that sets loading screen while downloading ct images and rt struct structures

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
        image_size = (1300, 900)
        image = QtGui.QImage(image_size[0], image_size[1], QtGui.QImage.Format_RGB32)
        image.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(image)
        font = QtGui.QFont("Arial", 45)
        painter.setFont(font)
        text_color = QtGui.QColor(QtCore.Qt.black)
        painter.setPen(text_color)
        image_width, image_height = image.width(), image.height()
        text = "Loading rt struct images, please wait..."
        text_width = painter.fontMetrics().width(text)
        text_height = painter.fontMetrics().height()
        text_x = (image_width - text_width) // 2
        text_y = (image_height - text_height) // 2
        painter.drawText(text_x, text_y, text)
        painter.end()

        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(
            self.pixmap.scaled(
                self.graphics_view.width(),
                self.graphics_view.height(),
                aspectRatioMode=QtCore.Qt.KeepAspectRatio,
            )
        )
        self.graphics_view.setScene(self.scene)
        self.graphics_view.show()

    def create_menu_bar(self) -> None:
        """
        Function which creates menu bar

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
        menuBar = self.menuBar()
        self.menuFile = menuBar.addMenu("&File")
        self.menuFileSave = QtWidgets.QAction("Save as")
        self.menuFileExit = QtWidgets.QAction("Exit")
        self.menuFile.addAction(self.menuFileSave)
        self.menuFile.addAction(self.menuFileExit)
        self.menuFileSave.setShortcut("Ctrl+S")
        self.menuFileExit.setShortcut("Ctrl+Q")
        self.menuFileSave.triggered.connect(self.saveImage)
        self.menuFileExit.triggered.connect(QtWidgets.qApp.quit)

    def saveImage(self) -> None:
        """
        Function that saves image in the given path by the user

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
        try:
            if self.merged_images:
                path = QtWidgets.QFileDialog(
                    caption="Save As", directory=os.path.expanduser("~/Desktop")
                )
                file = path.getSaveFileName(
                    self,
                    "Save Image",
                    "image.png",
                    "PNG (*.png);;TIF (*.tif);;TIFF (*.tiff);;BMP (*.bmp);;JPEG (*.jpeg);;JPG (*.jpg)",
                )
                image = contrast_enhancement(
                    self.merged_images[self.last_rolled_position],
                    self.current_window_center,
                    self.current_window_width,
                )
                cv2.imwrite(str(file[0]), image)
        except Exception as e:
            print("An error was encountered while saving an image" + str(e))

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Function that handles wheel mouse event and counts wheel movement distance

        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event.

        Returns
        -------
        Nothing

        """
        if self.merged_images:
            if len(self.merged_images) > 0:  # checking that the collection is not empty
                max_size = len(self.merged_images)
                # proper handling of the scroll button
                if event.angleDelta().y() > 0:
                    if self.last_rolled_position < max_size:
                        self.last_rolled_position += 1  # if we scroll up (increment)
                    if (
                        self.last_rolled_position + 1
                    ) == max_size:  # keeping an eye on whether or not we have gone beyond the number of available slices
                        self.last_rolled_position = 0
                elif event.angleDelta().y() < 0:
                    if self.last_rolled_position > 0:
                        self.last_rolled_position -= 1  # if we scroll down (decrement)
                    if self.last_rolled_position == 0:
                        self.last_rolled_position = (
                            max_size  # if we scroll down (decrement)
                        )

                if (
                    self.current_rolled_position != self.last_rolled_position
                ):  # change the current position if it is different
                    self.current_rolled_position = self.last_rolled_position
                    self.load_image(self.last_rolled_position)  # reloading the image

    def mouse_move_event(self, event: QtGui.QMouseEvent) -> None:
        """
        Function that handles moving mouse event and counts mouse movement distance

        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event.

        Returns
        -------
        Nothing

        """
        if (
            event.buttons() == QtCore.Qt.LeftButton
        ):  # detection if the left mouse button has been pressed
            self.window_center += (int)(
                (event.x() - self.last_x_position) / 100
            )  # setting the appropriate value window center
            self.window_width += (int)(
                (event.y() - self.last_y_position) / 100
            )  # setting the appropriate value window width

            # checking whether the adopted threshold is not exceeded (if so, then setting the maximum values)
            if self.window_center > 3095:
                self.window_center = 3095  # maximum value of window center

            if self.window_center < -1024:
                self.window_center = -1024  # maximum value of window center

            if self.window_width > 4096:
                self.window_width = 4096  # maximum value of window width

            if self.window_width < 1:
                self.window_width = 1  # maximum value of window width

            self.label_window_width.setText("Window width: " + str(self.window_width))
            self.label_window_center.setText(
                "Window center: " + str(self.window_center)
            )

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        """
        Function that handles press mouse event

        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event.

        Returns
        -------
        Nothing

        """
        self.last_x_position = event.x()
        self.last_y_position = event.y()

    def mouse_release_event(self, event: QtGui.QMouseEvent) -> None:
        """
        Function that handles moving mouse event

        Parameters
        ----------
        event : QtGui.QWheelEvent
            The QWheelEvent class contains parameters that describes a wheel event.

        Returns
        -------
        Nothing

        """
        self.last_x_position = (
            None  # set the variables to None when you release the mouse
        )
        self.last_y_position = None
        if self.merged_images:
            if (
                self.current_window_width != self.window_width
                or self.current_window_center != self.window_center
            ):  # checking if the window width, and window center values have changed
                self.current_window_width = self.window_width  # changing window width
                self.current_window_center = (
                    self.window_center
                )  # changing window center
                self.load_image(self.current_slice)

    def push_button_dicom_dir(self) -> None:
        """
        Function that handles button which opens ct scans directory

        Parameters
        ----------
        None

        Returns
        -------
        Nothing

        """
        try:
            if self.path_to_rt_file:
                self.set_loading_screen()
            path = (
                QtWidgets.QFileDialog.getExistingDirectory()
            )  # selecting the folder containing the ct files

            self.path_to_ct_dir = path + "/*.dcm"
            self.scene = QtWidgets.QGraphicsScene()
            if os.path.isdir(self.path_to_ct_dir):
                # find all files in the selected folder
                self.load_images_with_structures()
            if self.merged_images:
                self.label_slice_number.setText(
                    "Number of slice: "
                    + str(self.current_slice)
                    + "/"
                    + str(len(self.merged_images) - 1)
                )
            self.load_image(self.current_slice)
        except Exception as e:
            print(
                "An error was encountered while opening a folder with DICOM files: "
                + str(e)
            )

    def push_button_rtstruct_file(self) -> None:
        """
        Function that handles button which opens rtstruct structures file

        Parameters
        ----------
        None

        Returns
        -------
        Nothing

        """
        try:
            if self.path_to_ct_dir:
                self.set_loading_screen()
            self.path_to_rt_file = (
                QtWidgets.QFileDialog.getOpenFileName()
            )  # select the file (must be in a dicom format .dcm)
            self.path_to_rt_file = self.path_to_rt_file[0]

            if check_if_file_is_rt_struct_file(self.path_to_rt_file):
                self.load_images_with_structures()  # load image

            if self.merged_images:
                self.label_slice_number.setText(
                    "Number of slice: "
                    + str(self.current_slice)
                    + "/"
                    + str(len(self.merged_images) - 1)
                )
            self.load_image(self.current_slice)
        except Exception as e:
            print(
                "An error was encountered while opening a RTStruct structure file: "
                + str(e)
            )

    def load_images_with_structures(self) -> None:
        """
        Function that loads all images from paths given by the user

        Parameters
        ----------
        None

        Returns
        -------
        Nothing

        """
        if self.path_to_rt_file and self.path_to_ct_dir:
            self.setWindowTitle("Loading rt structures and ct images...")
            self.merged_images = list()
            self.rt_structures = list()
            (
                self.images_with_rt_structures,
                self.rt_struct_color,
            ) = load_ct_and_rtstruct_images(
                self.path_to_ct_dir,
                self.path_to_rt_file,
                self.window_width,
                self.window_center,
            )
            for pair in self.images_with_rt_structures:
                self.merged_images.append(pair[0])
                self.rt_structures.append(pair[1])
            self.setWindowTitle(
                "Software for visualization of RTStruct structures on CT images"
            )

    def load_image(self, number: int) -> None:
        """
        Function that loads current slice of ct scan with rt struct structures

        Parameters
        ----------
        number : int
            The slice number of the ct scan that is currently displayed

        Returns
        -------
        Nothing

        """
        try:
            if self.merged_images:
                if number >= 0 and number < len(self.merged_images):
                    self.current_slice = number  # setting the slice number
                    self.label_slice_number.setText(
                        "Number of slice: "
                        + str(self.current_slice)
                        + "/"
                        + str(len(self.merged_images) - 1)
                    )
                    image = self.merged_images[self.current_slice]

                    image = contrast_enhancement(
                        image, self.current_window_center, self.current_window_width
                    )

                    loaded_image = add_rt_struct_to_image(
                        image,
                        self.rt_structures[self.current_slice],
                        self.rt_struct_color,
                    )

                    # creating an image from data (using the Format_RGB888 format)
                    image = QtGui.QImage(
                        loaded_image.data,
                        loaded_image.shape[1],
                        loaded_image.shape[0],
                        loaded_image.strides[0],
                        QtGui.QImage.Format_RGB888,
                    )
                    self.pixmap = QtGui.QPixmap.fromImage(
                        image
                    )  # create a pixmap from a modified image
                    self.scene = QtWidgets.QGraphicsScene()
                    self.scene.addPixmap(
                        self.pixmap.scaled(
                            self.graphics_view.width() - 2,
                            self.graphics_view.height() - 2,
                            aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                        )
                    )  # scaling the view to the size of the widget
                    self.graphics_view.setScene(self.scene)  # setting scene
                    self.graphics_view.show()
        except Exception as e:
            print(
                f"An error was encountered while loading {self.current_slice} image: "
                + str(e)
            )
