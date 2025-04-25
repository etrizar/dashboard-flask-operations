from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)   # 🔵 Primero crear la app

# 🔵 Luego configurar la app
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
app.permanent_session_lifetime = timedelta(minutes=10)

PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'admin123')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password_input = request.form.get('password')
        if password_input == PASSWORD:
            session.permanent = True  # 🔵 Sesión permanente, sujeta a timeout
            session['authenticated'] = True

            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="❌ Contraseña incorrecta")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
