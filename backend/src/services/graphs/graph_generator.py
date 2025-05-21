import numpy as np
import plotly.graph_objects as go
import plotly.subplots as psub
import os
from datetime import datetime

def generate_graph6_no_prediction(test_img: np.ndarray) -> str:
    modalities = ['Modalidad T1c', 'Modalidad T2w', 'Modalidad FLAIR']
    modality_index = {modality: i for i, modality in enumerate(modalities)}

    fig = psub.make_subplots(
        rows=1, cols=len(modalities),
        subplot_titles=[f"Modalidad: {modality}" for modality in modalities],
        specs=[[{"type": "heatmap"}] * len(modalities)]
    )

    for idx, modality in enumerate(modalities):
        fig.add_trace(
            go.Heatmap(
                z=np.rot90(test_img[:, :, 0, modality_index[modality]]),
                colorscale='gray',
                showscale=False,
            ),
            row=1, col=idx + 1
        )

    frames = []
    for slice_index in range(test_img.shape[2]):
        frame_data = []
        for idx, modality in enumerate(modalities):
            frame_data.append(
                go.Heatmap(
                    z=np.rot90(test_img[:, :, slice_index, modality_index[modality]], k=-1),
                    colorscale='gray',
                    showscale=False,
                )
            )
        frames.append(go.Frame(data=frame_data, name=f"slice_{slice_index}"))

    fig.frames = frames

    steps = [
        dict(
            method="animate",
            args=[[f"slice_{i}"], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
            label=str(i)
        ) for i in range(test_img.shape[2])
    ]

    layout_updates = {
        "sliders": [dict(active=0, pad={"t": 50}, steps=steps)],
        "annotations": [dict(
            text="Desliza para cambiar entre rebanadas del cerebro",
            x=0.5, y=-0.15, xref="paper", yref="paper", showarrow=False,
            font=dict(size=12, color="black")
        )],
        "title": "Visualización interactiva de rebanadas (T1c, T2w y FLAIR)",
        "height": 500,
        "width": 1500,
        "autosize": True,
        "margin": dict(l=20, r=20, t=40, b=80),
        "plot_bgcolor": 'white'
    }

    for i in range(1, len(modalities) + 1):
        layout_updates[f'xaxis{i}'] = dict(showgrid=False, zeroline=False, visible=False)
        layout_updates[f'yaxis{i}'] = dict(showgrid=False, zeroline=False, visible=False)

    fig.update_layout(**layout_updates)

    filename = f"graph6_no_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    file_path = os.path.join('static', filename)
    fig.write_html(file_path)
    return filename
