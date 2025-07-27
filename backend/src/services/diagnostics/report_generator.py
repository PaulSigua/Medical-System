import os
import json
import pdfkit

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")


def find_folder_by_patient_id(patient_id: str) -> str:
    for folder in os.listdir(STATIC_DIR):
        if patient_id in folder:
            return folder
    raise FileNotFoundError(
        f"No se encontró carpeta para el paciente {patient_id}")


def generate_pdf_report(patient_id: str) -> str:
    folder_name = find_folder_by_patient_id(patient_id)
    html_dir = os.path.join(STATIC_DIR, folder_name, "html")
    output_path = os.path.join(
        STATIC_DIR, folder_name, f"{patient_id}_diagnosis_report.pdf")

    # Cargar imágenes
    img_seg_path = os.path.join(html_dir, "segmentation_summary.png")
    img_dist_path = os.path.join(html_dir, "class_distribution.png")

    if not os.path.exists(img_seg_path) or not os.path.exists(img_dist_path):
        raise FileNotFoundError("Imágenes necesarias no encontradas.")

    # Cargar métricas y explicación
    summary_path = os.path.join(html_dir, "summary.json")
    if not os.path.exists(summary_path):
        raise FileNotFoundError("No se encontró el archivo summary.json")

    with open(summary_path, "r", encoding="utf-8") as f:
        summary_data = json.load(f)

    explanation = summary_data.get(
        "explanation", "No se encontró explicación generada.")
    wt = summary_data.get("all_metrics", {}).get(
        "whole_tumor (WT)", {}).get("Accuracy", "N/A")
    tc = summary_data.get("all_metrics", {}).get(
        "tumor_core (TC)", {}).get("Accuracy", "N/A")
    et = summary_data.get("all_metrics", {}).get(
        "enhancing_tumor (ET)", {}).get("Accuracy", "N/A")

    # HTML base
    template_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            h1 {{
                color: #2b6cb0;
            }}
            .section {{
                margin-bottom: 30px;
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin-bottom: 20px;
                border: 1px solid #ccc;
            }}
            .metrics {{
                font-size: 16px;
            }}
            .explanation {{
                background: #f9f9f9;
                padding: 10px;
                border-left: 4px solid #2b6cb0;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <h1>Reporte de Segmentación Tumoral</h1>

        <div class="section">
            <h2>Paciente ID: {patient_id}</h2>
            <p>Este reporte resume los resultados obtenidos mediante IA para la segmentación tumoral automática.</p>
        </div>

        <div class="section metrics">
            <h3>Accuracy por clase:</h3>
            <ul>
                <li><strong>Whole Tumor (WT):</strong> {wt}</li>
                <li><strong>Tumor Core (TC):</strong> {tc}</li>
                <li><strong>Enhancing Tumor (ET):</strong> {et}</li>
            </ul>
        </div>

        <div class="section explanation">
            <h3>Explicación generada:</h3>
            <p>{explanation}</p>
        </div>
        
        <div class="section">
            <h3>Resumen gráfico de la segmentación</h3>
            <img src="file://{img_seg_path}" alt="Segmentación resumen">
        </div>

        <div class="section">
            <h3>Distribución de clases segmentadas</h3>
            <img src="file://{img_dist_path}" alt="Distribución de clases">
        </div>
    </body>
    </html>
    """

    # Guardar HTML temporal
    tmp_path = os.path.join(html_dir, "tmp_summary_report.html")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(template_html)

    # Generar PDF
    pdfkit.from_file(
        tmp_path,
        output_path,
        options={"enable-local-file-access": ""}
    )

    os.remove(tmp_path)

    return output_path
