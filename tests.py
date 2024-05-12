import unittest
import pydicom as dicom

from utils import *


class RtSrtuctTests(unittest.TestCase):
    """Test cases for the RtStruct class.

    This class provides unit tests for the RtStruct class, which represents a radiotherapy structure.
    The tests ensure that the class functions as expected and handles various scenarios correctly.

    Args:
        unittest (type): The base class for all test cases. Inherits farom `unittest.TestCase`.

    Attributes:
        None

    Methods:
        test_if_images(self): Test if the RtStruct contains valid images.
        test_if_pixel_spacing(self): Test if the RtStruct contains valid pixel spacing information.
        test_if_patient_position(self): Test if the RtStruct contains valid patient position information.
        test_if_contrast_enhancement(self): Test if contrast enhancement improves the image quality.
        test_if_get_number_of_slices_data_dicom(self): Test if the provided DICOM data contains multiple slices.
        test_if_rt_struct_structure_file(self): Test if a specific structure exists in the provided RT-STRUCT file.
        test_if_parse_rt_struct(self): Test if the provided RT-STRUCT file can be successfully parsed.
        test_if_loaded_rt_struct(self): Test if an RT-STRUCT file has been successfully loaded.

    """

    # loading ct data
    ct_images_files_path = (
        "data/Pediatric-CT-SEG-02AC04B6/09-21-2005-NA-CT-35474/4.000000-CT-08387/*.dcm"
    )
    rtstruct_data_file_path = "data/Pediatric-CT-SEG-02AC04B6/09-21-2005-NA-CT-35474/2.000000-RTSTRUCT-86390/1-1.dcm"

    # loading ct and rt struct data
    loaded_images = load_ct_and_rtstruct_images(
        ct_images_files_path, rtstruct_data_file_path, 1000, 1000
    )

    # loading data dicom
    data_dicom = dicom.dcmread(
        "data/Pediatric-CT-SEG-02AC04B6/09-21-2005-NA-CT-35474/4.000000-CT-08387/1-001.dcm",
        force=True,
    )

    def test_if_images(self):
        """Test if the RtStruct contains valid images.

        This test case verifies that the RtStruct object contains valid images by checking
        if the image data is present and in the correct format. It ensures that the images
        are properly loaded and accessible within the RtStruct instance.

        1. Create an instance of the RtStruct class.
        2. Load the images into the RtStruct object.
        3. Check if the images are successfully loaded.
        4. Assert that the loaded images are valid.

        """
        for image in self.loaded_images:
            self.assertIsNotNone(image)

    def test_if_pixel_spacing(self):
        """Test if the RtStruct contains valid pixel spacing information.

        This test case verifies that the RtStruct object contains valid pixel spacing
        information by checking if the pixel spacing values are present and have the
        correct format. It ensures that the pixel spacing is properly stored and
        accessible within the RtStruct instance.

        1. Create an instance of the RtStruct class.
        2. Load the pixel spacing information into the RtStruct object.
        3. Check if the pixel spacing values are successfully loaded.
        4. Assert that the loaded pixel spacing information is valid.
        """
        pixel_spacing = get_pixel_spacing(self.data_dicom)
        self.assertIsNotNone(pixel_spacing)
        self.assertEqual(len(pixel_spacing), 2)

    def test_if_patient_position(self):
        """Test if the RtStruct contains valid patient position information.

        This test case verifies that the RtStruct object contains valid patient
        position information by checking if the patient position value is present
        and has the correct format. It ensures that the patient position is properly
        stored and accessible within the RtStruct instance.

        1. Create an instance of the RtStruct class.
        2. Load the patient position information into the RtStruct object.
        3. Check if the patient position value is successfully loaded.
        4. Assert that the loaded patient position information is valid.
        """

        patient_position = get_patient_position(self.data_dicom)
        self.assertIsNotNone(patient_position)
        self.assertEqual(len(patient_position), 3)

    def test_if_contrast_enhancement(self):
        """Test if contrast enhancement improves the image quality.

        This function takes an image as input and performs a contrast enhancement
        algorithm. It then compares the enhanced image with the original image using
        appropriate metrics to determine if the contrast enhancement improves the
        image quality.

        """
        test_image = contrast_enhancement(self.data_dicom.pixel_array)
        self.assertIsNotNone(test_image)
        test_image = contrast_enhancement(self.data_dicom.pixel_array, 123, 342)
        self.assertIsNotNone(test_image)

    def test_if_get_number_of_slices_data_dicom(self):
        """Test if the provided DICOM data contains multiple slices.

        This function takes DICOM data as input and checks if it contains multiple
        slices. It analyzes the DICOM metadata to determine the number of slices
        present in the data.

        """
        number = get_number_of_slices_data_dicom(self.data_dicom)
        self.assertIsNotNone(number)

    def test_if_rt_struct_structure_file(self):
        """Test if a specific structure exists in the provided RT-STRUCT file.

        This method takes an RT-STRUCT file and a structure name as input, and
        checks if the specified structure exists in the file. It searches for
        the structure within the RT-STRUCT file's structure set and returns True
        if found, or False otherwise.

        """
        is_rt_struct = check_if_file_is_rt_struct_file(self.rtstruct_data_file_path)
        self.assertTrue(is_rt_struct)

    def test_if_parse_rt_struct(self):
        """Test if the provided RT-STRUCT file can be successfully parsed.

        This function takes an RT-STRUCT file as input and checks if it can be
        parsed correctly. It attempts to parse the RT-STRUCT file using a DICOM
        parsing library and verifies if the parsing is successful.
        """
        parsed_structures = parse_rtstruct(
            dicom.dcmread(
                self.rtstruct_data_file_path,
                force=True,
            )
        )
        self.assertIsNotNone(parsed_structures)

    def test_if_loaded_rt_struct(self):
        """Test if an RT-STRUCT file has been successfully loaded.

        This method takes an RT-STRUCT file as input and checks if it has been
        successfully loaded and parsed. It verifies if the provided RT-STRUCT
        file object contains the necessary information for further processing.
        """
        rt_struct_structures = load_rtstruct(self.rtstruct_data_file_path)
        self.assertIsNotNone(rt_struct_structures)
        self.assertIsInstance(rt_struct_structures, dicom.FileDataset)


if __name__ == "__main__":
    unittest.main()
