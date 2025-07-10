import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = "src/templates"

def generate_segmentation_slice_html(modality: np.ndarray, mask: np.ndarray, patient_id: str) -> str:
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

    # Mantener proporción real: ancho = alto en ambos subplots
    fig.update_yaxes(scaleanchor="x", row=1, col=1)
    fig.update_yaxes(scaleanchor="x", row=1, col=2)

    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("plot_template.html")
    html_content = template.render(patient_id=patient_id, plot_div=plot_div)

    return html_content
