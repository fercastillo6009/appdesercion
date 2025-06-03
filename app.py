# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd
import os  # necesario para obtener el puerto

app = Flask(__name__)
model = joblib.load("modelo_desercion.joblib")
columns = joblib.load("columnas_modelo.joblib")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        data_dict = {
            'semestre': int(form["semestre"]),
            'edad': int(form["edad"]),
            'promedio': float(form["promedio"]),
            'faltas': int(form["faltas"]),
            'horas_estudio': int(form["horas_estudio"]),
            'motivacion': int(form["motivacion"]),
            'tristeza': int(form["tristeza"]),
            'perdida_interes': int(form["perdida_interes"]),
            'concentracion': int(form["concentracion"]),
            'sueno': int(form["sueno"]),
            'autoestima': int(form["autoestima"]),
            'genero_Masculino': int(form["genero"] == "Masculino"),
            'genero_Femenino': int(form["genero"] == "Femenino"),
            'responsabilidades_Sí': int(form["responsabilidades"] == "Sí"),
            'responsabilidades_No': int(form["responsabilidades"] == "No"),
            'reprobado_Sí': int(form["reprobado"] == "Sí"),
            'reprobado_No': int(form["reprobado"] == "No"),
            'trabajo_Sí': int(form["trabajo"] == "Sí"),
            'trabajo_No': int(form["trabajo"] == "No"),
            'internet_Sí': int(form["internet"] == "Sí"),
            'internet_No': int(form["internet"] == "No"),
            'apoyo_Sí': int(form["apoyo"] == "Sí"),
            'apoyo_No': int(form["apoyo"] == "No"),
            'ambiente_Sí': int(form["ambiente"] == "Sí"),
            'ambiente_No': int(form["ambiente"] == "No"),
            'pensado_abandonar_Sí': int(form["abandono"] == "Sí"),
            'pensado_abandonar_No': int(form["abandono"] == "No"),
        }

        input_df = pd.DataFrame([data_dict])
        input_df = input_df.reindex(columns, axis=1, fill_value=0)
        prediction = model.predict(input_df)[0]

        resultado = "Desertará" if prediction == 1 else "No desertará"
        return render_template("formulario.html", resultado=resultado)

    return render_template("formulario.html", resultado=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
