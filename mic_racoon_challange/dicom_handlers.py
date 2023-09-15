import numpy as np
import pydicom
from pathlib import Path
import matplotlib.pyplot as plt
from .helpers import get_file_name, ensure_dir


# Function to normalize a numpy array
def normalize_np_arr(x: np.array):
    """
    Normalize the values of the input numpy array to the range [0, 1].

    Parameters:
    x (np.array): Input numpy array.

    Returns:
    np.array: Normalized numpy array.
    """
    x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x_norm


# Function to threshold a numpy array
def threshold_np_arr(x: np.array, threshold_val: float = 0.5):
    """
    Threshold the input numpy array based on a given threshold value.

    Parameters:
    x (np.array): Input numpy array.
    threshold_val (float): Threshold value (default is 0.5).

    Returns:
    np.array: Thresholded numpy array.
    """
    x[x <= threshold_val] = 0
    x[x > threshold_val] = 1
    return x.astype('uint16')


# Function to save a numpy array as a PNG image
def np_to_png(img_arr: np.array, output_path: str, filename: str):
    """
    Save a numpy array as a PNG image.

    Parameters:
    img_arr (np.array): Input numpy array.
    output_path (str): Output directory path.
    filename (str): Desired filename for the saved PNG image.
    """
    outfile = Path(output_path, f'{filename}.png')
    plt.imsave(outfile, img_arr, cmap='gray')


# Function to extract DICOM details
def get_dicom_details(dicom_path: str):
    """
    Extract DICOM image details such as image type, filename, and volume.

    Parameters:
    dicom_path (str): Path to the DICOM file.

    Returns:
    tuple: A tuple containing image type, filename, and volume.
    """
    medical_image = pydicom.dcmread(dicom_path)
    types = ', '.join(medical_image.ImageType)
    filename = Path(medical_image.filename).stem
    volume = calculate_dicom_volume(medical_image)
    return types, filename, volume


# Function to calculate DICOM volume
def calculate_dicom_volume(dicom: pydicom.FileDataset) -> float:
    """
    Calculate the volume in mm³ for a given DICOM image.

    Parameters:
    dicom (pydicom.FileDataset): DICOM image data.

    Returns:
    float: Calculated volume in mm³.
    """
    if not hasattr(dicom, "PixelSpacing"):
        return 0.000
    pixel_spacing = dicom.PixelSpacing
    slice_thickness = dicom.SliceThickness
    n_pixels = np.count_nonzero(dicom.pixel_array)
    vol_mm3 = pixel_spacing[0] * pixel_spacing[1] * slice_thickness * n_pixels
    return round(vol_mm3, 3)


# Function to process a DICOM image
def process_dicom(dicom_path: str, output_dir: str, threshold_val: float = 0.5) -> float:
    """
    Process a DICOM image by normalizing, thresholding, and saving as PNG and DICOM files.

    Parameters:
    dicom_path (str): Path to the DICOM file.
    output_dir (str): Output directory path.
    threshold_val (float): Threshold value (default is 0.5).

    Returns:
    float: Calculated volume in mm³.
    """
    medical_image = pydicom.dcmread(dicom_path)

    img_arr = normalize_np_arr(medical_image.pixel_array)
    img_arr = threshold_np_arr(img_arr, threshold_val)

    filename = get_file_name(dicom_path)
    dicom_export_path = Path(output_dir, 'dicoms')
    ensure_dir(dicom_export_path)
    png_export_path = Path(output_dir, 'pngs')
    ensure_dir(png_export_path)

    np_to_png(img_arr, str(png_export_path), filename)
    medical_image.PixelData = img_arr.tobytes()
    vol = calculate_dicom_volume(medical_image)
    medical_image.save_as(dicom_export_path / f'{filename}.dcm')

    return vol
