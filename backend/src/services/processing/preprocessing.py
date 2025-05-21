import nibabel as nib
import numpy as np
import h5py
from skimage.transform import resize
from sklearn.preprocessing import MinMaxScaler
import os

PROCESSED_FOLDER = "src/processed_files"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
TARGET_SHAPE = (128, 128, 128)

def load_and_normalize(path):
    img = nib.load(path).get_fdata()
    scaler = MinMaxScaler()
    return scaler.fit_transform(img.reshape(-1, img.shape[-1])).reshape(img.shape)

def process_images_for_segmentation(patient_id, t1ce, t2, flair):
    combined = np.stack([t1ce, t2, flair], axis=3)
    resized = resize(combined, TARGET_SHAPE, mode='constant', anti_aliasing=True)
    path = os.path.join(PROCESSED_FOLDER, f"{patient_id}.h5")
    with h5py.File(path, 'w') as f:
        f.create_dataset('images', data=resized, compression='gzip')

def process_images_for_classification(patient_id, t1, t1ce, t2, flair):
    combined = np.stack([t1, t1ce, t2, flair], axis=3)
    resized = resize(combined, TARGET_SHAPE, mode='constant', anti_aliasing=True)
    path = os.path.join(PROCESSED_FOLDER, f"{patient_id}_to_classify.h5")
    with h5py.File(path, 'w') as f:
        f.create_dataset('images', data=resized, compression='gzip')
