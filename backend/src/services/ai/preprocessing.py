import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from skimage.transform import resize

def load_nifti(path):
    return nib.load(path).get_fdata()

def normalize(image):
    scaler = MinMaxScaler()
    return scaler.fit_transform(image.reshape(-1, image.shape[-1])).reshape(image.shape)

def resize_modalities(modalities: dict, shape: tuple):
    return {mod: resize(img, shape, mode='constant', anti_aliasing=True) for mod, img in modalities.items()}
