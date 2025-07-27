from services.ai.tensorflow_segmentation import perform_segmentation as tf_segmentation
from services.ai.nnunet_segmentation import perform_segmentation as nnunet_segmentation

def perform_segmentation_dispatcher(modality_paths: dict, framework: str):
    if framework == "tensorflow":
        return tf_segmentation(modality_paths)
    elif framework == "nnunet":
        return nnunet_segmentation(modality_paths)
    else:
        raise ValueError(f"Framework '{framework}' no soportado.")