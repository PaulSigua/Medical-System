import numpy as np
import plotly.graph_objects as go
import plotly.subplots as psub
import os
from services.processing.load_model_h5 import load_hdf5_file
from skimage import measure
from datetime import datetime


STATIC_DIR = "src/static"

CLASS_NAMES = {
    1: 'Necrosis',
    2: 'Edema',
    3: 'Tumor Activo',

}

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

def generate_graph1(test_img: np.ndarray, test_prediction_argmax: np.ndarray) -> str:
    modalities = ['Modalidad T1c', 'Modalidad T2w', 'Modalidad FLAIR']
    fig = psub.make_subplots(
        rows=2, cols=2,
        subplot_titles=modalities + ['Predicción del Modelo de IA'],
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
            intensity=values, colorscale='Viridis',
            opacity=0.3, flatshading=True, name=f'{modality} Brain'
        ), row=idx // 2 + 1, col=idx % 2 + 1)

    full_brain_volume = test_img[..., 0]
    verts, faces, normals, values = measure.marching_cubes(full_brain_volume, level=np.mean(full_brain_volume), step_size=2)
    fig.add_trace(go.Mesh3d(
        x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        intensity=values, colorscale='Viridis',
        opacity=0.1, flatshading=True, name='Full Brain'
    ), row=2, col=2)

    unique_classes = np.unique(test_prediction_argmax)
    for cls in unique_classes:
        if cls == 0:
            continue
        verts, faces, normals, values = measure.marching_cubes(test_prediction_argmax == cls, level=0.5, step_size=2)
        color = {1: 'red', 2: 'green', 3: 'blue', 4: 'yellow'}.get(cls, 'gray')
        fig.add_trace(go.Mesh3d(
            x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
            i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
            color=color, opacity=0.5, flatshading=True,
            name=f'Segmentación {cls}'
        ), row=2, col=2)

    layout_scenes = {
        f"scene{i}": dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectratio=dict(x=1, y=1, z=1)
        ) for i in range(1, 5)
    }

    fig.update_layout(
        title="Visualización cerebral 3D para cada modalidad y segmentación prevista",
        height=1000, width=1200,
        margin=dict(l=20, r=20, t=40, b=20),
        **layout_scenes
    )

    graph1_html = f'graph1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, graph1_html))
    return graph1_html


def generate_graph2(test_prediction_argmax: np.ndarray) -> tuple[str, str]:
    resolution_mm_per_voxel = 1.0
    class_diameters_mm = []
    labels = []
    colors = []

    report_text = (
        "Reporte de Segmentación Predicha:\n"
        "Este reporte presenta los diámetros estimados para cada clase de la segmentación predicha en la imagen cerebral.\n"
        "Las clases se identificaron y midieron utilizando un modelo de predicción.\n\n"
        "Detalles de los diámetros por clase:\n"
    )

    for cls in np.unique(test_prediction_argmax):
        if cls == 0:
            continue
        coords = np.argwhere(test_prediction_argmax == cls)
        if coords.size == 0:
            diameter_mm = 0
        else:
            diameter_mm = np.linalg.norm(coords.max(axis=0) - coords.min(axis=0)) * resolution_mm_per_voxel

        class_name = CLASS_NAMES.get(cls, f'Clase {cls}')
        labels.append(class_name)
        class_diameters_mm.append(diameter_mm)
        colors.append({'Necrosis': 'red', 'Edema': 'green', 'Tumor Activo': 'blue'}.get(class_name, 'gray'))

        report_text += f"{class_name}: {diameter_mm:.2f} mm\n"

    fig = go.Figure(go.Bar(
        y=labels,
        x=class_diameters_mm,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{d:.2f} mm³' for d in class_diameters_mm],
        textposition='auto'
    ))

    fig.update_layout(
        title="Diámetros de las Clases en la Segmentación Predicha",
        xaxis_title="Diámetro (en mm)",
        yaxis_title="Clase",
        height=600,
        width=800
    )

    graph2_html = f'graph2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, graph2_html))
    return graph2_html, report_text

def generate_graph3(test_img, test_prediction_argmax):
    class_names = ["no Tumor", "Nucleo Necrotico", "Edema", "Nucleo Activo"]
    test_prediction_named = np.zeros_like(test_prediction_argmax, dtype=object)

    for i, name in enumerate(class_names):
        test_prediction_named[test_prediction_argmax == i] = name

    fig = psub.make_subplots(
        rows=1, cols=2,
        subplot_titles=("MR del Paciente", "Predicción realizada"),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}]]
    )

    fig.add_trace(go.Heatmap(z=test_img[:, :, 0, 1], colorscale='gray', showscale=False), row=1, col=1)
    fig.add_trace(go.Heatmap(z=test_prediction_argmax[:, :, 0], colorscale='Viridis',
                             text=test_prediction_named[:, :, 0], hoverinfo='text'), row=1, col=2)

    frames = [
        go.Frame(data=[
            go.Heatmap(z=test_img[:, :, i, 1], colorscale='gray', showscale=False),
            go.Heatmap(z=test_prediction_argmax[:, :, i], colorscale='Viridis',
                       text=test_prediction_named[:, :, i], hoverinfo='text')
        ], name=str(i))
        for i in range(test_img.shape[2])
    ]

    fig.frames = frames

    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=[dict(method="animate", args=[[str(i)], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))], label=str(i)) for i in range(test_img.shape[2])]
    )]

    fig.update_layout(
        sliders=sliders,
        updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)])])],
        title="Visualización interactiva de sectores",
        height=800, width=1200,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    filename = f'graph3_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, filename))
    return filename


def generate_graph4(test_img, test_prediction_argmax):
    class_names = ["no Tumor", "Nucleo Necrotico", "Edema", "Nucleo Activo"]
    test_prediction_named = np.zeros_like(test_prediction_argmax, dtype=object)

    for i, name in enumerate(class_names):
        test_prediction_named[test_prediction_argmax == i] = name

    fig = psub.make_subplots(
        rows=1, cols=2,
        subplot_titles=("MRI Paciente", "Segmentación"),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}]]
    )

    def get_slice(plane, slice_idx):
        if plane == 'Axial':
            return test_img[:, :, slice_idx, 1], test_prediction_argmax[:, :, slice_idx], test_prediction_named[:, :, slice_idx]
        elif plane == 'Coronal':
            return test_img[:, slice_idx, :, 1], test_prediction_argmax[slice_idx, :, :], test_prediction_named[slice_idx, :, :]
        elif plane == 'Sagittal':
            return test_img[slice_idx, :, :, 1], test_prediction_argmax[slice_idx, :, :], test_prediction_named[slice_idx, :, :]

    img_slice, seg_slice, seg_named_slice = get_slice('Axial', 0)

    fig.add_trace(go.Heatmap(z=img_slice, colorscale='gray', showscale=False), row=1, col=1)
    fig.add_trace(go.Heatmap(z=seg_slice, colorscale='Viridis', showscale=True, text=seg_named_slice, hoverinfo='text'), row=1, col=2)

    frames = []
    planes = ['Axial', 'Coronal', 'Sagittal']
    for plane in planes:
        for i in range(test_img.shape[2]):
            img_slice, seg_slice, seg_named_slice = get_slice(plane, i)
            frames.append(go.Frame(data=[
                go.Heatmap(z=img_slice, colorscale='gray', showscale=False),
                go.Heatmap(z=seg_slice, colorscale='Viridis', showscale=True, text=seg_named_slice, hoverinfo='text')
            ], name=f'{plane}_{i}'))

    fig.frames = frames

    sliders = [dict(
        steps=[dict(method='animate', args=[[f'{plane}_{i}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))], label=f'{plane} - Slice {i}')
               for plane in planes for i in range(test_img.shape[2])],
        currentvalue=dict(prefix='Rebanada: ')
    )]

    fig.update_layout(
        sliders=sliders,
        updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)])])],
        title="Visualización interactiva de cortes cerebrales",
        height=800, width=1200,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white'
    )

    filename = f'graph4_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, filename))
    return filename

def generate_graph5(test_img, test_prediction_argmax):
    # Crear la gráfica fija que muestra las clases presentes en cada slice
    classes_per_slice = []
    num_classes_per_slice = []
    class_names = ["no Tumor", "Nucleo Necrotico", "Edema", "Nucleo Activo"]
    for i in range(test_img.shape[2]):
        unique_classes = np.unique(test_prediction_argmax[:, :, i])
        relevant_classes = [class_names[c] for c in unique_classes if c != 0]
        classes_per_slice.append(relevant_classes)
        num_classes_per_slice.append(len(relevant_classes))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(test_img.shape[2])),
        y=num_classes_per_slice,
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title="Presencia de clase en cada segmentación",
        xaxis_title="Número de rebanada",
        yaxis_title="Número de clases",
        height=600,
        width=800
    )

    graph5_html = f'graph5_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, graph5_html))

    # Crear el texto descriptivo para el reporte médico
    report_text5 = "Reporte de Segmentación Predicha:\n"
    report_text5 += "Este reporte presenta las clases presentes en cada rebanada de la segmentación predicha.\n\n"
    report_text5 += "Resumen de las clases presentes por rebanada (omitiendo 'no Tumor'):\n"

    def summarize_slices(classes_per_slice):
        summary = []
        start = 0
        current_classes = classes_per_slice[0]

        for i in range(1, len(classes_per_slice)):
            if classes_per_slice[i] != current_classes:
                if current_classes:
                    summary.append((start, i - 1, current_classes))
                start = i
                current_classes = classes_per_slice[i]

        if current_classes:
            summary.append((start, len(classes_per_slice) - 1, current_classes))

        return summary

    slice_summary = summarize_slices(classes_per_slice)
    for start, end, classes in slice_summary:
        if start == end:
            report_text5 += f"Rebanada {start}: {', '.join(classes)}\n"
        else:
            report_text5 += f"Rebanadas {start} - {end}: {', '.join(classes)}\n"

    return graph5_html, report_text5

# Función para generar la sexta gráfica
def generate_graph6(test_img, test_prediction_argmax):
    import numpy as np
    import plotly.graph_objects as go
    import plotly.subplots as psub
    import os
    from datetime import datetime

    class_names = ["no Tumor", "Necrosis", "Edema", "Nucleo Activo"]
    modalities = ['Modalidad T1c', 'Modalidad T2w', 'Modalidad FLAIR']
    modality_index = {modality: i for i, modality in enumerate(modalities)}

    # Crear una copia de test_prediction_argmax con los nombres de las clases
    test_prediction_named = np.zeros_like(test_prediction_argmax, dtype=object)
    for i, name in enumerate(class_names):
        test_prediction_named[test_prediction_argmax == i] = name

    # Crear la figura inicial con dos subplots
    fig = psub.make_subplots(
        rows=1, cols=2,
        subplot_titles=("Imágenes Médicas del Paciente (MRI)", "Predicción del Modelo de IA"),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}]]
    )

    # Añadir trazas iniciales (modalidad T1c y primer slice por defecto) aplicando la rotación 90° en sentido horario
    fig.add_trace(
        go.Heatmap(
            z=np.rot90(test_img[:, :, 0, modality_index['Modalidad T1c']], k=-1),
            colorscale='gray',
            showscale=False
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Heatmap(
            z=np.rot90(test_prediction_argmax[:, :, 0], k=-1),
            showscale=True,
            colorscale='Viridis',
            text=np.rot90(test_prediction_named[:, :, 0], k=-1),
            hoverinfo='text'
        ),
        row=1, col=2
    )

    # Crear los frames para todas las combinaciones de modalidad y slice
    frames = []
    for modality in modalities:
        for slice_index in range(test_img.shape[2]):
            frames.append(go.Frame(
                data=[
                    go.Heatmap(
                        z=np.rot90(test_img[:, :, slice_index, modality_index[modality]], k=-1),
                        colorscale='gray',
                        showscale=False
                    ),
                    go.Heatmap(
                        z=np.rot90(test_prediction_argmax[:, :, slice_index], k=-1),
                        showscale=True,
                        colorscale='Viridis',
                        text=np.rot90(test_prediction_named[:, :, slice_index], k=-1),
                        hoverinfo='text'
                    )
                ],
                name=f"{modality}_{slice_index}"
            ))

    # Añadir los frames a la figura
    fig.frames = frames

    # Crear el slider
    steps = []
    for slice_index in range(test_img.shape[2]):
        step = dict(
            method="animate",
            args=[[f"{modalities[0]}_{slice_index}"],
                  dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=str(slice_index)
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=steps
    )]

    # Crear el menú de botones para seleccionar la modalidad
    updatemenus = [
        dict(
            buttons=[
                dict(label=modality, method='animate',
                     args=[[f"{modality}_{slice_index}" for slice_index in range(test_img.shape[2])],
                           dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))])
                for modality in modalities
            ],
            direction='down',
            showactive=True,
            x=0.5,
            xanchor='left',
            y=1.2,
            yanchor='top'
        )
    ]

    # Añadir textos explicativos (anotaciones)
    annotations = [
        dict(
            text="Selecciona una modalidad:",
            x=0.2, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12, color="black")
        ),
        dict(
            text="Desliza para cambiar de rebanada:",
            x=0.5, y=-0.15,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12, color="black")
        )
    ]

    # Actualizar el layout de la figura
    fig.update_layout(
        sliders=sliders,
        updatemenus=updatemenus,
        annotations=annotations,
        title="Visualización interactiva de rebanadas",
        height=800,
        width=1200,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        yaxis2=dict(showgrid=False)
    )

    # Guardar la gráfica como un archivo HTML
    graph6_html = f'graph6_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    fig.write_html(os.path.join(STATIC_DIR, graph6_html))
    return graph6_html