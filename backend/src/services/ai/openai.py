import openai, os

API_KEY=os.getenv("OPENAI_API_KEY")

def build_explanation_prompt(patient_id: str, metrics: dict, gradcam_stats: dict | None = None) -> str:
    all_metrics = metrics.get("all_metrics", {})

    score_dice_et = all_metrics.get("enhancing_tumor (ET)", {}).get("Accuracy")
    score_dice_wt = all_metrics.get("whole_tumor (WT)", {}).get("Accuracy")
    score_dice_tc = all_metrics.get("tumor_core (TC)", {}).get("Accuracy")

    gradcam_info = ""
    if gradcam_stats:
        loc = gradcam_stats.get("gradcam_max_location")
        gradcam_info = f"""
        Además, se ha utilizado Grad-CAM para analizar visualmente las regiones de atención del modelo:

        - Ubicación del pico de activación: {loc}

        Comenta como este pico de activación beneficia a la segmentación realizada.
        """

    return f"""
    Paciente: {patient_id}

    Resultados de segmentación automática del tumor cerebral:

    - Accuracy por clase:
      - Whole Tumor (WT): {score_dice_wt}
      - Tumor Core (TC): {score_dice_tc}
      - Enhancing Tumor (ET): {score_dice_et}

    Por favor, genera una explicación médica clara e interpretativa sobre estos valores de Score Dice.
    Evalúa el desempeño del modelo y su posible fiabilidad diagnóstica para cada clase.
    También comenta si estos resultados pueden ser considerados clínicamente útiles.
    Además, genera la respuesta de manera directa, por que está es una explicación de predicciones.

    {gradcam_info}
    """


client = openai.OpenAI(api_key=API_KEY)  # cliente moderno

def explain_prediction_with_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.4
    )

    return response.choices[0].message.content