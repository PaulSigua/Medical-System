<div align="center">

![UPS Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Logo_Universidad_Polit%C3%A9cnica_Salesiana_del_Ecuador.png/640px-Logo_Universidad_Polit%C3%A9cnica_Salesiana_del_Ecuador.png)

## Universidad Politécnica Salesiana  
## Computer Science Career
---
### **System for Supporting Brain Cancer Diagnosis**  
</div>

---

# 🧠 Medical System (Cranius AI) - AI-Assisted Segmentation and Diagnosis Platform

Prediction, segmentation, and explainability system for brain cancer diagnosis, developed as part of the graduation project at the **Universidad Politécnica Salesiana of Ecuador**.

## 📌 Description

This system allows doctors and healthcare professionals to upload medical images (T1, T1c, T2, and FLAIR modalities), perform automatic segmentations with artificial intelligence models (such as `nnU-Net`), visualize comparisons with manual segmentations, generate visual explanations (Grad-CAM), and produce clinical reports in PDF format.

---

## ⚙️ Technologies Used

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Angular + TailwindCSS
- **Deep Learning**: nnU-Net (v1), PyTorch
- **Visualization**: Plotly, Matplotlib
- **Image Storage**: NIfTI (.nii.gz)
- **Reports**: Embedded HTML + `pdfkit` + `wkhtmltopdf`
- **Additional scraping (optional)**: Selenium, BeautifulSoup

---

## 📂 Project Structure

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

## 🚀 Main Features

- [x] Upload of medical modalities (T1, T1c, T2, FLAIR)
- [x] Automatic segmentation with `nnU-Net`
- [x] Interactive visualization and Grad-CAM
- [x] Comparison with manual segmentation
- [x] Clinical PDF reports
- [x] User registration and authentication
- [x] Manual evaluation logging
- [x] Surveys to assess AI usefulness

---

## 🧪 Model Training

The model was trained on the **BraTS 2023 (ASNR-MICCAI)** dataset using `nnU-Net v1`.

To train with two modalities (for example, T1 and T1c), the following configuration was used:

```bash
nnUNet_plan_and_preprocess -t 501 --verify_dataset_integrity
nnUNet_train 2d nnUNetTrainerV2 501 0 --npz
```

> The data is organized in `nnUNet_raw/Task501_BrainTumour/` following the official format.

---

## 📄 Report Generation

Each patient has a unique folder (`YYYY-MM-DD_patient_id`) where the following files are stored:

- `segmentation_summary.png`
- `class_distribution.png`
- `report.html`
- `report.pdf`

---

## 🩺 Clinical Applications

- Support for brain tumor diagnosis
- Automatic vs. manual visual evaluation
- Full traceability per patient
- Statistical record of usage and medical feedback

---

## 🔒 Authentication and Permissions

The system allows authenticated user roles (doctor) for full access to patient modules, reports, image uploads, and AI evaluation.

---

## 📚 References

- [nnU-Net: Official Framework](https://github.com/MIC-DKFZ/nnUNet)
- [BraTS 2023 Dataset](https://www.synapse.org/#!Synapse:syn51068140)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [3D Slicer](https://www.slicer.org/)

---

## 👨‍⚕️ Authors

**Paúl Sigua, Jeison Pañora, and David Alvarado**, students of the Computer Science Engineering program  
Universidad Politécnica Salesiana – Ecuador  
Thesis supervised by: Ing. Remigio Hurtado, PhD

---

## 📃 License

This project is presented for academic purposes as part of a graduation project. All rights to the medical models and data used belong to their original authors.

*No files handled correspond to real patients. Tests with real patients were conducted in a controlled environment outside this repository.*
