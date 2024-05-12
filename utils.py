import cv2, glob
import pydicom as dicom
import numpy as np

# Default windowing parameters
WINDOW_WIDTH = 1000
WINDOW_CENTER = 1000


def load_rtstruct(file_path: str) -> dicom.FileDataset:
    """
    Function that loads rt struct structure from path given by the user

    Args:
        file_path (str): path to the file given by the user

    Returns:
        dicom.FileDataset: loaded rt struct structures from the given file
    """
    return dicom.dcmread(file_path, force=True)


def parse_rtstruct(rtstruct: dicom.FileDataset) -> tuple:
    """
    Function which parse rt structures and sorts them by Z axis

    Args:
        rtstruct (dicom.FileDataset): rt struct structures dataset given by the user

    Returns:
        tuple: tuple of rt struct structures and their color
    """
    rt_struct_elements = dict()

    for structure in rtstruct.ROIContourSequence:
        if "ContourSequence" in structure:
            for sequence in structure.ContourSequence:
                array = [
                    sequence.ContourData[i : i + 3]
                    for i in range(0, len(sequence.ContourData), 3)
                ]
                z = round(array[0][2], 2)  # rounding of the z element
                if z not in rt_struct_elements:
                    rt_struct_elements[z] = []
                rt_struct_elements[z] = array

    return rt_struct_elements, rtstruct.ROIContourSequence[0].ROIDisplayColor


def contrast_enhancement(
    image: np.ndarray,
    window_center: int = WINDOW_CENTER,
    window_width: int = WINDOW_WIDTH,
) -> np.ndarray:
    """
    Function that changes window center and window width of currently displayed image.

    Windowing, also known as grey-level mapping, contrast stretching, histogram modification
    or contrast enhancement is the process in which the CT image grayscale component of an
    image is manipulated via the CT numbers; doing this will change the appearance of the
    picture to highlight particular structures. The brightness of the image is adjusted via
    the window level. The contrast is adjusted via the window width.

    source: https://radiopaedia.org/articles/windowing-ct

    Args:
        image (np.ndarray): ct image without rt struct structures in gray scale
        window_center (int, optional): window center represents the gray value at the center of the window.
        Defaults to WINDOW_CENTER.
        window_width (int, optional): window width defines the range of gray values that will be displayed.
        Defaults to WINDOW_WIDTH.

    Returns:
        np.ndarray: converted image to a given contrast in RGB
    """
    image = (
        np.clip(image - (window_center - window_width / 2), 0, window_width - 1)
        * 256
        / window_width
    )
    image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    return image


def get_number_of_slices_data_dicom(data_dicom: dicom.FileDataset) -> int:
    """
    Function that returns number of slices that given dataset has

    Args:
        data_dicom (dicom.FileDataset): ct images from the dataset given by the user

    Returns:
        int: number of slices in the dataset
    """
    patient_center_position = data_dicom.ImagePositionPatient
    return patient_center_position[2]


def get_pixel_spacing(data_dicom: dicom.FileDataset) -> tuple:
    """
    Function that returns pixel spacing used in the dataset

    Args:
        data_dicom (dicom.FileDataset): ct images from the dataset given by the user

    Returns:
        tuple: pixel spacing for X,Y,Z axes
    """
    return tuple(data_dicom.PixelSpacing)


def get_patient_position(data_dicom: dicom.FileDataset) -> tuple:
    """
    Function that returns patient center position used in the dataset

    Args:
        data_dicom (dicom.FileDataset): ct images from the dataset given by the user

    Returns:
        tuple: patient center position (X,Y,Z)
    """
    return tuple(data_dicom.ImagePositionPatient)


def check_if_file_is_rt_struct_file(rtstructpath: str) -> bool:
    """
    Function which checks if given file is rt struct structure file

    Args:
        rtstructpath (str): rt struct file given by the user

    Returns:
        bool: flag which indicates whether file is an rt struct file
    """
    if ".dcm" in rtstructpath:  # checking if the file has the 'dcm' extension
        rtstruct = dicom.dcmread(
            rtstructpath, force=True
        )  # reading RTStruct structures from dicom file
        if "ROIContourSequence" in rtstruct:
            return True
        else:
            return False
    else:
        return False


def load_images_and_rtstruct_structures(
    rt_struct_elements: dict,
    data_dicom: dicom.FileDataset,
    patient_center_position: tuple,
    x_spacing: float,
    y_spacing: float,
) -> list:
    """
    Function which load images and rt struct structures

    Args:
        rt_struct_elements (dict): dictionary of rt struct elements sorted by Z axis
        data_dicom (dicom.FileDataset): ct images from the dataset given by the user
        patient_center_position (tuple): patient center position (X,Y,Z)
        x_spacing (float): pixel spacing for X axis
        y_spacing (float): pixel spacing for Y axis

    Returns:
        list: list of converted ct images with rt struct structures
    """
    images_and_structures = list()
    for scan in rt_struct_elements:
        if patient_center_position[2] == scan:
            # information about image as numpy.ndarray
            image = data_dicom.pixel_array
            structure = list()

            for scan in rt_struct_elements:
                if patient_center_position[2] == scan:
                    for scan in rt_struct_elements:
                        if patient_center_position[2] == scan:
                            for x, y, _ in rt_struct_elements[scan]:
                                x = int((x - patient_center_position[0]) / x_spacing)
                                y = int((y - patient_center_position[1]) / y_spacing)
                                structure.append((x, y))
            images_and_structures.append((image, structure))

    return images_and_structures


def add_rt_struct_to_image(
    image: cv2.Mat, rtstructures: list, rt_struct_color: tuple
) -> cv2.Mat:
    """
    Add rt struct structures to the image with given color

    Args:
        image (cv2.Mat): raw ct image slice
        rtstructures (list): rt struct structures as list of (X,Y) points
        rt_struct_color (tuple): given color of rt struct structures

    Returns:
        cv2.Mat: converted ct image with rt struct structures
    """
    for x, y in rtstructures:
        image = cv2.circle(
            image,
            (x, y),
            radius=0,
            color=rt_struct_color,
            thickness=4,
        )

    return image


def load_ct_and_rtstruct_images(
    folder_path_ct: str, folder_path_rt: str, window_width: int, window_center: int
) -> tuple:
    """
    Function which load images and rt struct structures

    Args:
        folder_path_ct (str): path to the ct images directory, given by the user
        folder_path_rt (str): path to the rt struct structure file, given by the user
        window_center (int): window center represents the gray value at the center of the window.
        window_width (int): window width defines the range of gray values that will be displayed.

    Returns:
        tuple: of converted ct images with rt struct structures and color of rt struct structure
    """
    rtstruct = load_rtstruct(folder_path_rt)
    rt_struct_elements, rt_struct_color = parse_rtstruct(rtstruct)

    image_and_structures_list = list()

    for image_path in glob.glob(folder_path_ct):
        data_dicom = dicom.dcmread(image_path, force=True)  # reading dicom file
        patient_center_position = get_patient_position(data_dicom)
        x_spacing, y_spacing = get_pixel_spacing(data_dicom)

        image_and_structures_list += load_images_and_rtstruct_structures(
            rt_struct_elements,
            data_dicom,
            patient_center_position,
            x_spacing,
            y_spacing,
        )

    return image_and_structures_list, rt_struct_color
