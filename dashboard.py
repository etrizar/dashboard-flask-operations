from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        archivo = 'registro_operaciones.csv'

        if not os.path.exists(archivo):
            return "⚠️ No hay datos de operaciones registrados aún."

        df = pd.read_csv(archivo)

        total_operaciones = len(df)
        operaciones_ganadoras = len(df[df['GananciaPerdida(USD)'] > 0])
        operaciones_perdedoras = len(df[df['GananciaPerdida(USD)'] <= 0])
        ganancia_total = df['GananciaPerdida(USD)'].sum()
        porcentaje_acierto = (operaciones_ganadoras / total_operaciones) * 100 if total_operaciones > 0 else 0

        labels = df['FechaHora'].tolist()
        ganancias = df['GananciaPerdida(USD)'].tolist()

        return render_template('dashboard.html',
                               total_operaciones=total_operaciones,
                               operaciones_ganadoras=operaciones_ganadoras,
                               operaciones_perdedoras=operaciones_perdedoras,
                               ganancia_total=ganancia_total,
                               porcentaje_acierto=porcentaje_acierto,
                               labels=labels,
                               ganancias=ganancias)

    except Exception as e:
        return f"❌ Error cargando datos: {e}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
