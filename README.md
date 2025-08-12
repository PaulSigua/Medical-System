<div align="center">

![UPS Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Logo_Universidad_Polit%C3%A9cnica_Salesiana_del_Ecuador.png/640px-Logo_Universidad_Polit%C3%A9cnica_Salesiana_del_Ecuador.png)

## Universidad Politécnica Salesiana  
## Carrera de Ciencias de la Computación  
---
### **Sistema para el apoyo en el diagnóstico de cancer cerebral**  
</div>

---

# 🧠 Medical System (Cranius AI) - Plataforma de Segmentación y Diagnóstico Asistido por IA

Sistema de predicción, segmentación y explicación para el diagnóstico de cáncer cerebral, desarrollado como parte del trabajo de titulación de la **Universidad Politécnica Salesiana del Ecuador**.

## 📌 Descripción

Este sistema permite a médicos y profesionales de la salud cargar imágenes médicas (modalidades T1, T1c, T2 y FLAIR), realizar segmentaciones automáticas con modelos de inteligencia artificial (como `nnU-Net`), visualizar comparaciones con segmentaciones manuales, generar explicaciones visuales (Grad-CAM) y producir reportes clínicos en PDF.

---

## ⚙️ Tecnologías utilizadas

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Angular + TailwindCSS
- **Deep Learning**: nnU-Net (v1), PyTorch
- **Visualización**: Plotly, Matplotlib
- **Almacenamiento de imágenes**: NIfTI (.nii.gz)
- **Reportes**: HTML embebido + `pdfkit` + `wkhtmltopdf`
- **Scraping adicional (opcional)**: Selenium, BeautifulSoup

---

## 📂 Estructura del proyecto

```bash
Medical-System/
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── static/
├── frontend/
│   └── src/
│       └── app/
│           ├── components/
│           ├── pages/
│           └── services/
├── nnUNet_raw/
├── nnUNet_results/
├── scripts/
├── requirements.txt
└── README.md
```

---

## 🚀 Funcionalidades principales

- [x] Carga de modalidades médicas (T1, T1c, T2, FLAIR)
- [x] Segmentación automática con `nnU-Net`
- [x] Visualización interactiva y Grad-CAM
- [x] Comparación con segmentación manual
- [x] Reportes clínicos en PDF
- [x] Registro y autenticación de usuarios
- [x] Registro de evaluaciones manuales
- [x] Encuestas para evaluar utilidad de la IA

---

## 🧪 Entrenamiento del modelo

El modelo fue entrenado sobre el dataset **BraTS 2023 (ASNR-MICCAI)** utilizando `nnU-Net v1`.

Para entrenar con dos modalidades (por ejemplo, T1 y T1c), se utilizó la siguiente configuración:

```bash
nnUNet_plan_and_preprocess -t 501 --verify_dataset_integrity
nnUNet_train 2d nnUNetTrainerV2 501 0 --npz
```

> Los datos se encuentran organizados en `nnUNet_raw/Task501_BrainTumour/` según el formato oficial.

---

## 📄 Generación de Reportes

Cada paciente cuenta con una carpeta única (`YYYY-MM-DD_patient_id`) donde se almacenan:

- `segmentation_summary.png`
- `class_distribution.png`
- `report.html`
- `report.pdf`

---

## 🩺 Aplicaciones clínicas

- Soporte al diagnóstico de tumores cerebrales
- Evaluación visual automática vs. manual
- Trazabilidad completa por paciente
- Registro estadístico de uso y retroalimentación médica

---

## 🔒 Autenticación y permisos

El sistema permite roles de usuario autenticado (médico) para acceso completo a los módulos de pacientes, reportes, carga de imágenes y evaluación de IA.

---

## 📚 Referencias

- [nnU-Net: Framework oficial](https://github.com/MIC-DKFZ/nnUNet)
- [BraTS 2023 Dataset](https://www.synapse.org/#!Synapse:syn51068140)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [3D Slicer](https://www.slicer.org/)

---

## 👨‍⚕️ Autores

**Paúl Sigua, Jeison Pañora y David Alvarado**, estudiantes de la carrera de Ingeniería en Ciencias de la Computación  
Universidad Politécnica Salesiana – Ecuador  
Tesis dirigida por: Ing. Remigio Hurtado, PhD

---

## 📃 Licencia

Este proyecto se presenta con fines académicos como parte de un trabajo de titulación. Todos los derechos sobre los modelos médicos y datos utilizados corresponden a sus autores originales.

*Ningún archivo manejado corresponde a pacientes reales. Las pruebas con pacientes reales se realizaron en un entorno controlado fuera de este repositorio.*