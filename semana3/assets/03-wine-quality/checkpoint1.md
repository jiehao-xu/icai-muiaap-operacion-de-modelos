1. ¿Qué campo identifica la muestra?
sample_id
2. ¿Qué once campos consume el modelo?
fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide, total_sulfur_dioxide,density,ph,sulphates,alcohol
3. Proponed una nueva columna que el contrato debería rechazar.
nif_paciente
4. Proponed dos valores inválidos y explicad por qué.
alcohol: 200. Un numero demasiado elevado, se encuentra fuera del rango
fixed_acidity: -1.0. No puede haber números negativos