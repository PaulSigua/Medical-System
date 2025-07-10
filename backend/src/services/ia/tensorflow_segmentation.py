import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv3DTranspose
from .preprocessing import load_nifti, normalize, resize_modalities

MODEL_PATH = "src/models/ai/models_segmentation/segmentation_brats_modelUnet3D_3.h5"
EXPECTED_SHAPE = (128, 128, 128)

def custom_Conv3DTranspose(*args, **kwargs):
    kwargs.pop('groups', None)
    return Conv3DTranspose(*args, **kwargs)

model = load_model(MODEL_PATH, custom_objects={'Conv3DTranspose': custom_Conv3DTranspose})

def perform_segmentation(modality_paths: dict):
    modalities = ['T1c', 'T2W', 'T2F']
    images = {m: normalize(load_nifti(modality_paths[m])) for m in modalities}
    resized = resize_modalities(images, EXPECTED_SHAPE)

    tensor = np.stack([resized[m] for m in modalities], axis=-1)
    tensor = np.expand_dims(tensor, axis=0)

    result = model.predict(tensor)
    return np.argmax(result, axis=4)[0]
