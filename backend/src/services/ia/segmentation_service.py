import os
import numpy as np
import nibabel as nib
import h5py
import plotly.graph_objects as go
from skimage.transform import resize
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv3DTranspose

from uuid import uuid4

BASE_DIR = "src/processed_files"
SEGMENTATION_MODEL_PATH = "src/models/ia/models_segmentation/segmentation_brats_modelUnet3D_3.h5"
EXPECTED_SHAPE = (128, 128, 128)

# Aseguramos que el directorio de salida exista
os.makedirs(BASE_DIR, exist_ok=True)

# Conv3DTranspose personalizado
def custom_Conv3DTranspose(*args, **kwargs):
    kwargs.pop('groups', None)
    return Conv3DTranspose(*args, **kwargs)

# Cargar modelo una vez
segmentation_model = load_model(SEGMENTATION_MODEL_PATH, custom_objects={'Conv3DTranspose': custom_Conv3DTranspose})

def load_nifti(file_path):
    return nib.load(file_path).get_fdata()

def normalize(image):
    scaler = MinMaxScaler()
    return scaler.fit_transform(image.reshape(-1, image.shape[-1])).reshape(image.shape)

def resize_modalities(modalities: dict):
    return {mod: resize(img, EXPECTED_SHAPE, mode='constant', anti_aliasing=True)
            for mod, img in modalities.items()}

def perform_segmentation(modalities_paths: dict):
    required_modalities = ['T1c', 'T2W', 'T2F']
    images = {mod: normalize(load_nifti(modalities_paths[mod])) for mod in required_modalities}
    resized = resize_modalities(images)

    input_tensor = np.stack([resized['T1c'], resized['T2W'], resized['T2F']], axis=-1)
    input_tensor = np.expand_dims(input_tensor, axis=0)

    result = segmentation_model.predict(input_tensor)
    segmentation = np.argmax(result, axis=4)[0]

    return segmentation

def generate_segmentation_3d_plot(segmentation, patient_id: str):
    try:
        # Crear una gráfica interactiva 3D con Plotly
        colors = ['rgba(0,0,0,0)', 'green', 'blue', 'red']
        labels = ['Fondo', 'Necrosis', 'Edema', 'Realzado']
        fig = go.Figure()

        for i, label in enumerate(labels[1:], start=1):
            mask = (segmentation == i)
            x, y, z = np.where(mask)
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=dict(size=2, color=colors[i]),
                name=label
            ))

        fig.update_layout(
            title="Segmentación tumoral 3D",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        output_path = os.path.join(BASE_DIR, f"segmentation_{patient_id}_{uuid4().hex}.html")
        fig.write_html(output_path)
        return output_path
    except Exception as e:
        print(f"")
        return str("Error al generar la gráfica 3D: " + str(e))