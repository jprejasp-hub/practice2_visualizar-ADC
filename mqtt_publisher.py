import serial
import paho.mqtt.client as mqtt
import time

# Configuración Arduino
PUERTO = "/dev/cu.usbserial-11220"
BAUDIOS = 9600

# Configuración MQTT
BROKER = "broker.hivemq.com"
PUERTO_MQTT = 1883
TOPICO = "upch/practica2/adc/monitor_01"

# Conectar con MQTT
cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

cliente.connect(BROKER, PUERTO_MQTT, 60)
cliente.loop_start()

# Conectar con Arduino
arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Arduino conectado")
print("Enviando datos ADC mediante MQTT...")

try:
    while True:
        linea = arduino.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        try:
            adc = int(linea)

            if 0 <= adc <= 1023:
                cliente.publish(TOPICO, str(adc))
                print(f"ADC enviado: {adc}")

        except ValueError:
            continue

except KeyboardInterrupt:
    print("Transmisión finalizada")

finally:
    arduino.close()
    cliente.loop_stop()
    cliente.disconnect()
