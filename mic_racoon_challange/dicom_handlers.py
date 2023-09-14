import numpy as np
import pydicom
from pathlib import Path
import matplotlib.pyplot as plt
from .helpers import get_file_name, ensure_dir


def normalize_np_arr(x: np.array):
    # normalize all values to be between 0 and 1
    x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x_norm


def threshold_np_arr(x: np.array, threshold_val: float = 0.5):
    x[x < threshold_val] = 0
    x[x >= threshold_val] = 1
    return x.astype('uint16')


def np_to_png(img_arr: np.array, output_path: str, filename: str):
    outfile = Path(output_path, f'{filename}.png')
    plt.imsave(outfile, img_arr, cmap='gray')


def get_dicom_details(dicom_path: str):
    medical_image = pydicom.dcmread(dicom_path)
    types = ', '.join(medical_image.ImageType)
    filename = Path(medical_image.filename).stem
    print(filename)
    return types, filename


def process_dicom(dicom_path: str, output_dir: str, threshold_val: float = 0.5):
    medical_image = pydicom.read_file(dicom_path)
    img_arr = normalize_np_arr(medical_image.pixel_array)
    img_arr = threshold_np_arr(img_arr, threshold_val)

    filename = get_file_name(dicom_path)
    dicom_export_path = Path(output_dir, 'dicoms')
    ensure_dir(dicom_export_path)
    png_export_path = Path(output_dir, 'pngs')
    ensure_dir(png_export_path)

    np_to_png(img_arr, str(png_export_path), filename)
    medical_image.PixelData = img_arr.tobytes()
    medical_image.save_as(dicom_export_path / f'{filename}.dcm')

    return
