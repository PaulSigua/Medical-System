import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jinja2 import Environment, FileSystemLoader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TEMPLATE_DIR = "src/templates"

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
                    z=modality[:, :, z],
                    zmin=0,
                    zmax=1,
                    colorscale='gray',
                    showscale=False
                ),
                go.Heatmap(
                    z=mask[:, :, z],
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
        z=modality[:, :, 0],
        zmin=0,
        zmax=1,
        colorscale='gray',
        showscale=False
    ), row=1, col=1)

    fig.add_trace(go.Heatmap(
        z=mask[:, :, 0],
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

def generate_summary_png(image: np.ndarray, mask: np.ndarray, output_path: str, modality_name="FLAIR"):
    slice_index = image.shape[2] // 2  # Cortar al medio

    labels = {
        1: ("edema", "Reds"),
        2: ("non-enhancing tumor", "Blues"),
        3: ("enhancing tumour", "Greens")
    }

    plt.figure(figsize=(16, 4))

    # Imagen original
    plt.subplot(1, len(labels) + 1, 1)
    plt.imshow(image[:, :, slice_index], cmap="gray")
    plt.title(f"Modalidad ({modality_name})")
    plt.axis("off")

    # Máscaras superpuestas
    for i, (label_val, (label_name, cmap)) in enumerate(labels.items(), start=2):
        binary_mask = (mask[:, :, slice_index] == label_val)
        plt.subplot(1, len(labels) + 1, i)
        plt.imshow(image[:, :, slice_index], cmap="gray")
        plt.imshow(binary_mask, cmap=cmap, alpha=0.6)
        plt.title(label_name)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_class_distribution(mask, save_path):
    labels = {1: "Edema", 2: "Non-Enhancing", 3: "Enhancing"}
    counts = [(mask == i).sum() for i in labels]
    
    plt.figure(figsize=(6, 4))
    plt.bar(labels.values(), counts, color=['red', 'blue', 'green'])
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

    # Orientación BraTS (axial = [x,y,z], coronal = [x,z,y], sagital = [y,z,x])
    if orientation == "coronal":
        modality_img = modality_img.transpose(0, 2, 1)
        auto_seg = auto_seg.transpose(0, 2, 1)
        manual_seg = manual_seg.transpose(0, 2, 1)
    elif orientation == "sagittal":
        modality_img = modality_img.transpose(1, 2, 0)
        auto_seg = auto_seg.transpose(1, 2, 0)
        manual_seg = manual_seg.transpose(1, 2, 0)
    # Axial (default) = [x,y,z], no transposición

    modality_img, auto_seg = pad_to_same_shape(modality_img, auto_seg)
    modality_img, manual_seg = pad_to_same_shape(modality_img, manual_seg)

    COLORSCALE_SEG = [
        [0.0, "rgba(0,0,0,0)"],        # fondo
        [0.33, "rgba(255,0,0,0.6)"],   # edema
        [0.66, "rgba(0,255,0,0.6)"],   # non-enhancing
        [1.0, "rgba(0,0,255,0.6)"]     # enhancing
    ]

    depth = modality_img.shape[2]
    frames = []
    for z in range(depth):
        frames.append(go.Frame(data=[
            go.Heatmap(z=modality_img[:, :, z], zmin=0, zmax=1, colorscale='gray', showscale=False),
            go.Heatmap(z=auto_seg[:, :, z], zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False),
            go.Heatmap(z=manual_seg[:, :, z], zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False)
        ], name=str(z)))

    fig = make_subplots(rows=1, cols=3, subplot_titles=[
        f"{modality.upper()} ({orientation})", "Modelo", "Médico"
    ])

    fig.add_trace(go.Heatmap(z=modality_img[:, :, 0], zmin=0, zmax=1, colorscale='gray', showscale=False), 1, 1)
    fig.add_trace(go.Heatmap(z=auto_seg[:, :, 0], zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False), 1, 2)
    fig.add_trace(go.Heatmap(z=manual_seg[:, :, 0], zmin=0, zmax=3, colorscale=COLORSCALE_SEG, showscale=False), 1, 3)

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

    # Escala cuadrada estilo BraTS
    for i in range(1, 4):
        fig.update_yaxes(scaleanchor=f"x{i}", row=1, col=i)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("plot_template.html")
    return template.render(
        patient_id=patient_id,
        plot_div=fig.to_html(full_html=False, include_plotlyjs='cdn')
    )
