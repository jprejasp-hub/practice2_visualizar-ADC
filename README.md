# Monitor ADC - Arduino UNO | MQTT | Streamlit
#### Implementación de un sistema de adquisición, transmisión y visualización de señales analógicas mediante ARDUINO UNO, un potenciómetro y una aplicación web desarrollada en Python con Streamlit.
## El Arduino adquiere los valores del potenciómetro mediante su conversor analógico-digital (ADC) de 10 bits, generando lecturas entre 0 y 1023.
## Los datos se transmiten por comunicación serial a Python, que los publica mediante el protocolo MQTT utilizando un broker público. Finalmente, una aplicación desplegada en Streamlit Community Cloud recibe los mensajes y representa las lecturas mediante una gráfica dinámica (st.line_chart).
## Tecnologías utilizadas:
* Hardware: Arduino UNO y potenciómetro.
* Programación: Arduino IDE (C/C++) y Python.
* Comunicación: Serial USB y protocolo MQTT.
* Broker MQTT: HiveMQ público.
* Visualización: Streamlit y Pandas.
* Control de versiones: GitHub.
## Este prototipo demuestra una arquitectura básica de adquisición y monitoreo remoto de señales, aplicable como fundamento para el desarrollo de soluciones de Internet de las Cosas (IoT), telesalud y monitoreo de variables biomédicas.
## Proyecto académico – Maestría en Tecnologías Avanzadas para la Salud 
## Link: https://practice2visualizaradc.streamlit.app 
