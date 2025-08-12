import os
import torch
import numpy as np
import nibabel as nib
from nnunet.training.network_training.nnUNetTrainerV2 import nnUNetTrainerV2
from torch.nn.functional import pad, softmax
from scipy.ndimage import zoom, gaussian_filter

def generate_gradcam_nifti(patient_id: str, upload_folder: str, class_index: int = 1) -> str:
    # === 1. Configuración ===
    task = "Task501_BrainTumour"
    plans = "nnUNetPlansv2.1"
    trainer_name = "nnUNetTrainerV2"
    fold = 0
    model_dir = os.path.join(os.environ["RESULTS_FOLDER"], "nnUNet", "3d_fullres", task, f"{trainer_name}__{plans}", f"fold_{fold}")
    dataset_dir = os.path.join(os.environ["nnUNet_preprocessed"], task)

    # === 2. Cargar modelo ===
    trainer = nnUNetTrainerV2(
        plans_file=os.path.join(model_dir, "../plans.pkl"),
        fold=fold,
        output_folder=model_dir,
        dataset_directory=dataset_dir
    )

    torch.serialization.add_safe_globals([
        np.core.multiarray.scalar,
        np.dtype,
        np.float32,
        np.int64,
        np.complex64,
        np.bool_,
    ])

    trainer.initialize(training=False)
    state_dict = torch.load(os.path.join(model_dir, "model_best.model"), map_location="cuda", weights_only=False)
    trainer.network.load_state_dict(state_dict['state_dict'])
    model = trainer.network.eval().cuda()

    # === 3. Cargar input ===
    input_dir = os.path.join("src", "uploads", upload_folder, "nnunet_input")
    case_id = "case_0000"
    modalities = ["0000", "0001", "0002", "0003"]
    volume_np = [nib.load(os.path.join(input_dir, f"{case_id}_{m}.nii.gz")).get_fdata() for m in modalities]
    volume_np = np.stack(volume_np)
    input_tensor = torch.from_numpy(volume_np).unsqueeze(0).float().cuda()

    # === 4. Hooks ===
    activations, gradients = {}, {}
    def fwd_hook(module, input, output): activations['value'] = output.detach()
    def bwd_hook(module, grad_input, grad_output): gradients['value'] = grad_output[0].detach()
    target_layer = model.conv_blocks_context[-1]
    target_layer.register_forward_hook(fwd_hook)
    target_layer.register_full_backward_hook(bwd_hook)

    # === 5. Padding y forward ===
    def pad_or_crop(tensor, shape):
        _, _, z, y, x = tensor.shape
        tz, ty, tx = shape
        return pad(tensor, (0, tx - x, 0, ty - y, 0, tz - z), mode='constant')[:, :, :tz, :ty, :tx]

    input_tensor = pad_or_crop(input_tensor, trainer.patch_size)
    input_tensor.requires_grad = True

    with torch.enable_grad():
        output_logits = model(input_tensor)

    if isinstance(output_logits, tuple):
        output_logits = output_logits[0]

    output_softmax = softmax(output_logits, dim=1)

    # Clase objetivo: score completo sin enmascarar
    class_score = output_softmax[0, class_index].sum()
    model.zero_grad()
    class_score.backward()

    # === 6. Grad-CAM (mejorado para visualización) ===
    act = activations['value'][0].cpu().numpy()  # (F, Z, Y, X)
    grad = gradients['value'][0].cpu().numpy()

    weights = np.mean(grad, axis=(1, 2, 3))  # GAP
    weights = np.maximum(weights, 0)  # ReLU sobre pesos

    cam = np.sum(weights[:, None, None, None] * act, axis=0)  # (Z, Y, X)
    cam = np.maximum(cam, 0)
    cam = gaussian_filter(cam, sigma=1)  # Suavizado opcional
    cam /= np.max(cam) + 1e-8

    # === 7. Resize a forma original ===
    target_shape = volume_np.shape[1:]  # (Z, Y, X)
    cam_resized = zoom(cam, np.array(target_shape) / np.array(cam.shape), order=1)

    # === 8. Guardar NIfTI ===
    t1c_path = os.path.join(input_dir, "case_0000_0002.nii.gz")
    affine = nib.load(t1c_path).affine
    cam_nifti = nib.Nifti1Image(cam_resized, affine)
    output_path = os.path.join("src", "processed_files", f"{patient_id}_gradcam_class{class_index}.nii.gz")
    nib.save(cam_nifti, output_path)

    # === 9. Métricas de validación ===
    threshold = 0.7
    cam_mask = cam_resized > threshold
    tumor_mask = (cam_resized > 0.1)

    intersection = np.logical_and(cam_mask, tumor_mask).sum()
    union = np.logical_or(cam_mask, tumor_mask).sum()
    iou = float(intersection / union) if union > 0 else 0.0
    max_index = np.unravel_index(np.argmax(cam_resized), cam_resized.shape)

    stats = {
        "gradcam_max_location": tuple(int(x) for x in max_index),
        "gradcam_iou_estimate": iou
    }

    return output_path, cam_resized, nib.load(t1c_path).get_fdata(), stats
