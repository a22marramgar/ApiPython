import json
import time
import pandas as pd
from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calcular_porcentaje(respuestas):
    respuestas_correctas = sum(respuesta['esCorrecta'] for respuesta in respuestas)
    total_respuestas = len(respuestas)
    porcentaje = (respuestas_correctas / total_respuestas) * 100
    return porcentaje

def createStats(data):
    df = pd.DataFrame(data)
    # Crear un DataFrame separado para las respuestas seleccionadas
    respuestas_df = pd.concat([pd.DataFrame(r) for r in df['respostes']], ignore_index=True)
    
    # Agrupar las respuestas por ID y calcular el porcentaje de respuestas correctas
    respuestas_agrupadas = respuestas_df.groupby('id')['esCorrecta'].mean() * 100
    json_data = json.loads(respuestas_agrupadas.to_json(orient='index'))
    print(json_data)

    # Mostrar el número de respuestas enviadas
    count_respuestas = len(df)
    json_data['Respuestas enviadas'] = count_respuestas

    # Mostrar el promedio de tiempo
    promedio_tiempo = df['tiempo'].mean()
    json_data['Tiempo promedio de respuestas'] = promedio_tiempo

    return json_data

@app.route("/create-stats", methods=["POST"])
def create_user():
    data = request.get_json()
    respuesta = createStats(data)
    
    return respuesta, 200

if __name__ == "__main__":
    app.run(debug=True)