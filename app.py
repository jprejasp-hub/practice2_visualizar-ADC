
import streamlit as st
import serial
import pandas as pd
import time

st.set_page_config(page_title="Monitor ADC", layout="wide")
st.title("Monitor ADC - Arduino UNO")
st.write("Visualización del potenciómetro en tiempo real")

puerto = st.text_input(
    "Puerto serial",
    "/dev/cu.usbserial-11220"
)

if "datos" not in st.session_state:
    st.session_state.datos = []

if st.button("Iniciar monitoreo"):
    try:
        arduino = serial.Serial(puerto, 9600, timeout=1)
        time.sleep(2)

        grafico = st.empty()
        indicador = st.empty()

        for i in range(300):
            linea = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            try:
                valor = int(linea)
                if not 0 <= valor <= 1023:
                    continue
            except ValueError:
                continue

            st.session_state.datos.append(valor)

            indicador.metric("ADC actual", valor)

            df = pd.DataFrame({
                "ADC": st.session_state.datos[-100:]
            })

            grafico.line_chart(
    df,
    y="ADC"
)

        arduino.close()
        st.success("Monitoreo finalizado")

    except serial.SerialException as e:
        st.error(f"Error de conexión: {e}")
