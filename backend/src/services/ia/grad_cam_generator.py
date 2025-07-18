import os
import torch
import numpy as np
import nibabel as nib
from nnunet.training.network_training.nnUNetTrainerV2 import nnUNetTrainerV2
from torch.nn.functional import pad, softmax
from scipy.ndimage import zoom

def generate_gradcam_nifti(patient_id: str, upload_folder: str, class_index: int = 1) -> str:
    # # === 1. Configuración ===
    # os.environ["nnUNet_raw_data_base"] = "/ruta/a/nnUNet_raw_data_base/nnUNet_raw_data"
    # os.environ["nnUNet_preprocessed"] = "/ruta/a/nnUNet_preprocessed"
    # os.environ["RESULTS_FOLDER"] = "/ruta/a/nnUNet_trained_models"

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

    # Parches para PyTorch >= 2.6
    import torch
    import numpy as np

    torch.serialization.add_safe_globals([
        np.core.multiarray.scalar,
        np.dtype,
        np.float32,
        np.int64,
        np.complex64,
        np.bool_,
    ])

    trainer.initialize(training=False)

    # Cargar modelo manualmente sin usar `load_checkpoint(...)`
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
    with torch.enable_grad():
        output_logits = model(input_tensor)
    if isinstance(output_logits, tuple):
        output_logits = output_logits[0]
    output_softmax = softmax(output_logits, dim=1)
    pred_classes = torch.argmax(output_softmax, dim=1)
    mask_class = (pred_classes == class_index).float()
    class_score = (output_softmax[0, class_index] * mask_class[0]).sum()
    model.zero_grad()
    class_score.backward()

    # === 6. Grad-CAM ===
    act = activations['value'][0].cpu().numpy()  # (F, Z, Y, X)
    grad = gradients['value'][0].cpu().numpy()
    weights = np.mean(grad, axis=(1, 2, 3))
    cam = np.sum(weights[:, None, None, None] * act, axis=0)
    cam = np.maximum(cam, 0)
    cam /= np.max(cam) + 1e-8

    # === 7. Resize ===
    target_shape = volume_np.shape[1:]  # (Z, Y, X)
    cam_resized = zoom(cam, np.array(target_shape) / np.array(cam.shape), order=1)

    # === 8. Guardar NIfTI ===
    t1c_path = os.path.join(input_dir, "case_0000_0002.nii.gz")  # Correcto
    affine = nib.load(t1c_path).affine
    cam_nifti = nib.Nifti1Image(cam_resized, affine)
    output_path = os.path.join("src", "processed_files", f"{patient_id}_gradcam_class{class_index}.nii.gz")
    nib.save(cam_nifti, output_path)

    return output_path, cam_resized, nib.load(t1c_path).get_fdata()
