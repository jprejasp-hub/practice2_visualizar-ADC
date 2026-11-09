import streamlit as st
import pandas as pd
import paho.mqtt.client as mqtt
import threading
import time
from collections import deque

# CONFIGURACIÓN
BROKER = "broker.hivemq.com"
PUERTO_MQTT = 1883
TOPICO = "upch/practica2/adc/monitor_01"

st.set_page_config(
    page_title="Monitor ADC - Arduino UNO",
    layout="wide"
)

# ALMACENAMIENTO COMPARTIDO
@st.cache_resource
def iniciar_mqtt():
    datos = deque(maxlen=100)
    estado = {
        "conectado": False,
        "ultimo_adc": None,
        "ultima_lectura": None,
        "error": None
    }
    bloqueo = threading.Lock()

    def on_connect(client, userdata, flags, reason_code, properties):
        with bloqueo:
            estado["conectado"] = not reason_code.is_failure

        if not reason_code.is_failure:
            client.subscribe(TOPICO)

    def on_disconnect(client, userdata, disconnect_flags,
                      reason_code, properties):
        with bloqueo:
            estado["conectado"] = False

    def on_message(client, userdata, msg):
        try:
            adc = int(msg.payload.decode("utf-8").strip())

            if 0 <= adc <= 1023:
                with bloqueo:
                    datos.append(adc)
                    estado["ultimo_adc"] = adc
                    estado["ultima_lectura"] = time.time()

        except (ValueError, UnicodeDecodeError):
            pass

    cliente = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    cliente.on_connect = on_connect
    cliente.on_disconnect = on_disconnect
    cliente.on_message = on_message

    try:
        cliente.connect(BROKER, PUERTO_MQTT, 60)
        cliente.loop_start()
    except Exception as e:
        estado["error"] = str(e)

    return datos, estado, bloqueo, cliente


datos, estado, bloqueo, cliente = iniciar_mqtt()

# INTERFAZ
st.title("Monitor ADC - Arduino UNO")
st.write("Visualización de lecturas ADC recibidas mediante MQTT")

st.caption(f"Broker: {BROKER} | Tópico: {TOPICO}")

@st.fragment(run_every=1)
def mostrar_monitor():

    with bloqueo:
        valores = list(datos)
        conectado = estado["conectado"]
        ultimo_adc = estado["ultimo_adc"]
        ultima_lectura = estado["ultima_lectura"]
        error = estado["error"]

    if error:
        st.error(f"Error MQTT: {error}")

    elif conectado:
        st.success("Conectado al broker MQTT")
    else:
        st.warning("Conectando al broker MQTT...")

    if ultima_lectura is None:
        st.info("Esperando lecturas ADC del Arduino...")

    elif time.time() - ultima_lectura > 5:
        st.warning(
            "Sin lecturas recientes. "
            "El Arduino puede estar desconectado."
        )

    if ultimo_adc is not None:
        st.metric("Último valor ADC recibido", ultimo_adc)
    else:
        st.metric("Último valor ADC recibido", "—")

    if valores:
        df = pd.DataFrame({"ADC": valores})
        st.line_chart(df, y="ADC")

    st.caption(
        "Rango ADC: 0–1023 | "
        "Actualización de pantalla: cada segundo"
    )


mostrar_monitor()
