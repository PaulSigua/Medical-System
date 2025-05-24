import numpy as np
import plotly.graph_objects as go
import plotly.subplots as psub
import os
from services.processing.load_model_h5 import load_hdf5_file
from skimage import measure

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Fuente Inter -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    html, body {{
      margin: 0; padding: 0;
      width: 100%; height: 100%;
      font-family: 'Inter', sans-serif;
      background-color: #ffffff;
      overflow: hidden;
    }}
    #chart {{
      width: 100%; height: 100%;
    }}
  </style>
</head>
<body>
  <div id="chart">
    {plot_div}
  </div>
</body>
</html>
"""

def write_responsive_html(fig, file_path: str, title: str):
    # genera sólo el div de la gráfica, responsive y con Plotly desde CDN
    plot_div = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={'responsive': True}
    )
    html = HTML_TEMPLATE.format(title=title, plot_div=plot_div)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_graph6_no_prediction(test_img: np.ndarray, patient_id: str) -> str:
    modalities = ['T1c', 'T2w', 'FLAIR']
    static_dir = os.path.join("src", "static")
    os.makedirs(static_dir, exist_ok=True)
    filename = f"{patient_id}_graph6.html"
    file_path = os.path.join(static_dir, filename)
    if os.path.exists(file_path):
        return filename

    # heatmaps en subplot
    fig = psub.make_subplots(
      rows=1, cols=3,
      subplot_titles=[f"Modalidad {m}" for m in modalities],
      specs=[[{"type":"heatmap"}]*3]
    )
    for i, m in enumerate(modalities):
        heat = go.Heatmap(
            z=np.rot90(test_img[:,:,0,i]),
            colorscale='gray',
            showscale=False
        )
        fig.add_trace(heat, row=1, col=i+1)

    # frames para animación
    frames = []
    for sl in range(test_img.shape[2]):
        data = [
            go.Heatmap(z=np.rot90(test_img[:,:,sl,i]), showscale=False)
            for i in range(3)
        ]
        frames.append(go.Frame(data=data, name=f"{sl}"))
    fig.frames = frames

    # slider steps
    steps = [
      dict(method="animate",
           args=[[str(i)],
                 dict(frame=dict(duration=0, redraw=True), mode="immediate")],
           label=str(i))
      for i in range(test_img.shape[2])
    ]

    fig.update_layout(
      title=dict(
        text="Visualización interactiva de rebanadas (T1c, T2w y FLAIR)",
        x=0.5, xanchor="center",
        font=dict(size=22, family="Inter")
      ),
      font=dict(family="Inter", size=14, color="#333"),
      margin=dict(l=10, r=10, t=60, b=60),
      autosize=True,
      sliders=[dict(active=0, pad={"t":30}, steps=steps)],
      paper_bgcolor="white",
      plot_bgcolor="white"
    )
    # oculta ejes
    for ax in range(1, 4):
        fig.update_xaxes(visible=False, row=1, col=ax)
        fig.update_yaxes(visible=False, row=1, col=ax)

    # escribe HTML responsivo
    write_responsive_html(fig, file_path, "Graph - Rebanadas")
    return filename

def generate_graph3d_diagnostic(h5_filepath: str, patient_id: str) -> str:
    test_img = load_hdf5_file(h5_filepath)
    if test_img is None:
        raise ValueError("Error al cargar el archivo HDF5.")

    modalities = ['Modalidad T1c', 'Modalidad T2w', 'Modalidad FLAIR']
    fig = psub.make_subplots(
        rows=2, cols=2,
        subplot_titles=modalities + ['Full Brain'],
        specs=[[{'type': 'scene'}, {'type': 'scene'}],
               [{'type': 'scene'}, {'type': 'scene'}]],
        horizontal_spacing=0.05,
        vertical_spacing=0.1
    )

    for idx, modality in enumerate(modalities):
        volume = test_img[..., idx]
        verts, faces, normals, values = measure.marching_cubes(volume, level=np.mean(volume), step_size=2)
        fig.add_trace(go.Mesh3d(
            x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
            i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
            intensity=values, colorscale='Viridis', opacity=0.3, flatshading=True, name=f'{modality} Brain'
        ), row=idx // 2 + 1, col=idx % 2 + 1)

    full_brain_volume = test_img[..., 0]
    verts, faces, normals, values = measure.marching_cubes(full_brain_volume, level=np.mean(full_brain_volume), step_size=2)
    fig.add_trace(go.Mesh3d(
        x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        intensity=values, colorscale='Viridis', opacity=0.1, flatshading=True, name='Full Brain'
    ), row=2, col=2)

    fig.update_layout(
        title={
            "text": "Visualización cerebral 3D para cada modalidad",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(family="Inter, sans-serif", size=24, color="#333")
        },
        height=1000, width=1500,
        font=dict(family="Inter, sans-serif", size=14, color="#333"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=60, b=20),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        scene2=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        scene3=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        scene4=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
    )

    html_filename = f"{patient_id}_graph3D_diagnostic.html"
    output_path = os.path.join("src", "static", html_filename)
    fig.write_html(output_path)

    return html_filename