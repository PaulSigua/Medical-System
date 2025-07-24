import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jinja2 import Environment, FileSystemLoader
import matplotlib, cv2
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TEMPLATE_DIR = "src/templates"

# Reorienta una imagen axial como en BraTS (vista desde los pies del paciente)
def orient_brats(slice_2d: np.ndarray) -> np.ndarray:
    return np.flipud(np.rot90(slice_2d, k=1))

# Para visualización en Matplotlib
def orient_brats_matplotlib(slice_2d: np.ndarray) -> np.ndarray:
    return np.rot90(slice_2d, k=1)

def pad_to_same_shape(modality: np.ndarray, mask: np.ndarray):
    h1, w1, _ = modality.shape
    h2, w2, _ = mask.shape

    target_h = max(h1, h2)
    target_w = max(w1, w2)

    def pad(array, target_h, target_w):
        pad_h = target_h - array.shape[0]
        pad_w = target_w - array.shape[1]
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left
        return np.pad(array, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), mode='constant')

    modality_padded = pad(modality, target_h, target_w)
    mask_padded = pad(mask, target_h, target_w)

    return modality_padded, mask_padded

def generate_segmentation_slice_html(modality: np.ndarray, mask: np.ndarray, patient_id: str) -> str:
    modality, mask = pad_to_same_shape(modality, mask)
    depth = min(modality.shape[2], mask.shape[2])
    frames = []

    for z in range(depth):
        frame = go.Frame(
            data=[
                go.Heatmap(
                    z=orient_brats(modality[:, :, z]),
                    zmin=0,
                    zmax=1,
                    colorscale='gray',
                    showscale=False
                ),
                go.Heatmap(
                    z=orient_brats(mask[:, :, z]),
                    zmin=0,
                    zmax=3,
                    colorscale='Viridis',
                    opacity=1,
                    showscale=False
                )
            ],
            name=str(z)
        )
        frames.append(frame)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("MR del Paciente", "Predicción"))

    fig.add_trace(go.Heatmap(
        z=orient_brats(modality[:, :, 0]),
        zmin=0,
        zmax=1,
        colorscale='gray',
        showscale=False
    ), row=1, col=1)

    fig.add_trace(go.Heatmap(
        z=orient_brats(mask[:, :, 0]),
        zmin=0,
        zmax=3,
        colorscale='Viridis',
        showscale=True
    ), row=1, col=2)

    fig.frames = frames

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
            }]
        }],
        sliders=[{
            "steps": [
                {"label": str(z), "method": "animate", "args": [[str(z)], {"mode": "immediate"}]}
                for z in range(depth)
            ],
            "currentvalue": {"prefix": "Slice: "}
        }]
    )

    # Forzar proporción igualada
    fig.update_yaxes(scaleanchor="x", row=1, col=1)
    fig.update_yaxes(scaleanchor="x", row=1, col=2)

    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("plot_template.html")
    html_content = template.render(patient_id=patient_id, plot_div=plot_div)

    return html_content

def generate_modalities_segmentation_png(
    modalities: dict,
    mask: np.ndarray,
    output_path: str
):
    """
    modalities: dict con claves ['T1', 'T1c', 'T2', 'Flair'] y valores np.ndarray
    mask: máscara de segmentación (3D)
    output_path: ruta del archivo PNG a guardar
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # === Slice central ===
    slice_index = mask.shape[2] // 2

    # === Colores RGBA por clase ===
    label_colors = {
        1: (0, 0, 1, 0.6),    # non-enhancing (azul)
        2: (0, 1, 0, 0.6),    # edema (verde)
        3: (1, 1, 0, 0.6),   # enhancing (amarillo)
    }

    fig, axes = plt.subplots(len(modalities), 2, figsize=(8, 10))
    fig.suptitle("Segmentación por modalidad y método de red neuronal", fontsize=14)

    for i, (modality_name, volume) in enumerate(modalities.items()):
        # Extraer el slice
        raw_img_slice = volume[:, :, slice_index]
        raw_mask_slice = mask[:, :, slice_index]

        # Reorientar ambos al estilo BraTS (vista desde los pies)
        img_slice = orient_brats_matplotlib(raw_img_slice)
        mask_slice = orient_brats_matplotlib(raw_mask_slice)

        # === Columna izquierda: imagen original ===
        ax_left = axes[i, 0]
        ax_left.imshow(img_slice, cmap="gray")
        ax_left.set_title(modality_name)
        ax_left.axis("off")

        # === Columna derecha: imagen + overlay de segmentación ===
        ax_right = axes[i, 1]
        ax_right.imshow(img_slice, cmap="gray")

        overlay = np.zeros((*mask_slice.shape, 4))
        for label_val, color in label_colors.items():
            overlay[mask_slice == label_val] = color

        ax_right.imshow(overlay)
        ax_right.set_title("Segmentación")
        ax_right.axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def plot_class_distribution(mask, save_path):
    labels = {1: "Edema", 2: "Non-Enhancing", 3: "Enhancing"}
    counts = [(mask == i).sum() for i in labels]
    
    plt.figure(figsize=(6, 4))
    plt.bar(labels.values(), counts, color=['green', 'blue', 'yellow'])
    plt.title("Distribución de Voxeles Segmentados por Clase")
    plt.ylabel("Número de voxeles")
    plt.tight_layout()
    plt.savefig(save_path)

def plot_class_volume_by_slice(mask, save_path):
    depth = mask.shape[2]
    volume_curves = {i: [] for i in [1, 2, 3]}

    for z in range(depth):
        for label in volume_curves:
            volume_curves[label].append((mask[:, :, z] == label).sum())

    plt.figure(figsize=(10, 4))
    for label, values in volume_curves.items():
        plt.plot(values, label=f"Clase {label}")
    
    plt.title("Evolución por corte axial")
    plt.xlabel("Slice")
    plt.ylabel("Área segmentada")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)

def generate_comparison_html(
    flair: np.ndarray,
    t1c: np.ndarray,
    auto_seg: np.ndarray,
    manual_seg: np.ndarray,
    patient_id: str,
    modality: str = "flair",
    orientation: str = "axial"
) -> str:
    modality_img = flair if modality == "flair" else t1c

    # Reorientación espacial
    if orientation == "coronal":
        modality_img = modality_img.transpose(0, 2, 1)
        auto_seg = auto_seg.transpose(0, 2, 1)
        manual_seg = manual_seg.transpose(0, 2, 1)
    elif orientation == "sagittal":
        modality_img = modality_img.transpose(1, 2, 0)
        auto_seg = auto_seg.transpose(1, 2, 0)
        manual_seg = manual_seg.transpose(1, 2, 0)

    # Asegurar mismo tamaño
    modality_img, auto_seg = pad_to_same_shape(modality_img, auto_seg)
    modality_img, manual_seg = pad_to_same_shape(modality_img, manual_seg)

    # Colores unificados
    COLORSCALE_SEG = [
        [0.0, "rgba(0,0,0,0)"],         # fondo
        [0.33, "rgba(255,255,0,0.6)"],  # edema - amarillo
        [0.66, "rgba(0,255,0,0.6)"],    # non-enhancing - verde
        [1.0, "rgba(0,0,255,0.6)"]      # enhancing - azul
    ]

    depth = modality_img.shape[2]
    frames = []

    for z in range(depth):
        frames.append(go.Frame(data=[
            go.Heatmap(z=orient_brats(modality_img[:, :, z]), zmin=0, zmax=1, colorscale='gray', showscale=False),
            go.Heatmap(z=orient_brats(auto_seg[:, :, z]), zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False),
            go.Heatmap(z=orient_brats(manual_seg[:, :, z]), zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False)
        ], name=str(z)))

    fig = make_subplots(rows=1, cols=3, subplot_titles=[
        f"{modality.upper()} ({orientation})", "Modelo", "Médico"
    ])

    fig.add_trace(go.Heatmap(z=orient_brats(modality_img[:, :, 0]), zmin=0, zmax=1, colorscale='gray', showscale=False), 1, 1)
    fig.add_trace(go.Heatmap(z=orient_brats(auto_seg[:, :, 0]), zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False), 1, 2)
    fig.add_trace(go.Heatmap(z=orient_brats(manual_seg[:, :, 0]), zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False), 1, 3)

    fig.frames = frames
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        width=1000,
        height=400,
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
            }]
        }],
        sliders=[{
            "steps": [{"label": str(z), "method": "animate", "args": [[str(z)], {"mode": "immediate"}]} for z in range(depth)],
            "currentvalue": {"prefix": "Slice: "}
        }]
    )

    for i in range(1, 4):
        fig.update_yaxes(scaleanchor=f"x{i}", row=1, col=i)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("plot_template.html")
    return template.render(
        patient_id=patient_id,
        plot_div=fig.to_html(full_html=False, include_plotlyjs='cdn')
    )

def generate_gradcam_overlay_html(
    cam_volume: np.ndarray,
    modality_volume: np.ndarray,
    patient_id: str,
    orientation: str = "axial"
) -> str:
    from jinja2 import Environment, FileSystemLoader
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Reorientar según el plano
    if orientation == "coronal":
        cam_volume = cam_volume.transpose(0, 2, 1)
        modality_volume = modality_volume.transpose(0, 2, 1)
    elif orientation == "sagittal":
        cam_volume = cam_volume.transpose(1, 2, 0)
        modality_volume = modality_volume.transpose(1, 2, 0)

    # Normalización
    cam_norm = cam_volume / (np.max(cam_volume) + 1e-8)
    modality_norm = (modality_volume - modality_volume.min()) / (modality_volume.max() - modality_volume.min() + 1e-8)

    depth = cam_volume.shape[2]
    frames = []

    for z in range(depth):
        frames.append(go.Frame(data=[
            go.Heatmap(
                z=orient_brats(modality_norm[:, :, z]),
                colorscale="gray",
                showscale=False
            ),
            go.Heatmap(
                z=np.fliplr(orient_brats(cam_norm[:, :, z])),  # ✅ solo invertir Grad-CAM
                colorscale="jet",
                opacity=0.6,
                showscale=False
            ),
        ], name=str(z)))

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Heatmap(
        z=orient_brats(modality_norm[:, :, 0]),
        colorscale="gray",
        showscale=False
    ), row=1, col=1)

    fig.add_trace(go.Heatmap(
        z=np.fliplr(orient_brats(cam_norm[:, :, 0])),  # ✅ solo invertir Grad-CAM
        colorscale="jet",
        opacity=0.6,
        showscale=True
    ), row=1, col=1)

    fig.frames = frames
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        width=600,
        height=500,
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
            }]
        }],
        sliders=[{
            "steps": [{"label": str(z), "method": "animate", "args": [[str(z)], {"mode": "immediate"}]} for z in range(depth)],
            "currentvalue": {"prefix": "Slice: "}
        }]
    )

    fig.update_yaxes(scaleanchor="x", row=1, col=1)

    # Renderizar en plantilla
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("plot_template.html")
    return template.render(patient_id=patient_id, plot_div=fig.to_html(full_html=False, include_plotlyjs='cdn'))
