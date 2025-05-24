import nibabel as nib
import numpy as np
import h5py
from skimage.transform import resize
from sklearn.preprocessing import MinMaxScaler
import os

PROCESSED_FOLDER = "src/processed_files"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
# print("Ruta absoluta de PROCESSED_FOLDER:", os.path.abspath(PROCESSED_FOLDER))
TARGET_SHAPE = (128, 128, 128)

def load_and_normalize(path):
    print(f"Cargando: {path}")
    img = nib.load(path).get_fdata()
    if img.size == 0:
        raise ValueError(f"Imagen vacía: {path}")
    print(f"Imagen cargada: {img.shape}")
    img_reshaped = img.reshape(-1, 1)
    scaler = MinMaxScaler()
    norm_img = scaler.fit_transform(img_reshaped).reshape(img.shape)
    return norm_img

def process_images_for_segmentation(patient_id, t1ce, t2, flair):
    print("Procesando segmentación...")
    combined = np.stack([t1ce, t2, flair], axis=3)
    resized = resize(combined, TARGET_SHAPE, mode='constant', anti_aliasing=True)
    path = os.path.join(PROCESSED_FOLDER, f"{patient_id}.h5")
    print(f"Guardando archivo H5 en: {path}")
    with h5py.File(path, 'w') as f:
        f.create_dataset('images', data=resized, compression='gzip')
    print("Archivo de segmentación guardado.")

def process_images_for_classification(patient_id, t1, t1ce, t2, flair):
    print("Procesando clasificación...")
    combined = np.stack([t1, t1ce, t2, flair], axis=3)
    resized = resize(combined, TARGET_SHAPE, mode='constant', anti_aliasing=True)
    path = os.path.join(PROCESSED_FOLDER, f"{patient_id}_to_classify.h5")
    print(f"Guardando archivo H5 en: {path}")
    with h5py.File(path, 'w') as f:
        f.create_dataset('images', data=resized, compression='gzip')
    print("Archivo de clasificación guardado.")
