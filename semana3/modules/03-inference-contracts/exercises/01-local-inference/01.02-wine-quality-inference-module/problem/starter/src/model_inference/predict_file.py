"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.

input_path = "../assets/inference_sample.csv"
output_path = "../aasets/inference_sample_predict.csv"

df = pd.read_csv(input_path)

X = preprocess_dataframe(df)

predictions = infer_wine_quality(X)

result = df.copy()
result["prediction"] = predictions

result.to_csv(output_path, index=False)
