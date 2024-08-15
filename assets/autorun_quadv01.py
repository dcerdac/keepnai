from dronekit import connect, VehicleMode
import time
import cv2

# Conectar con el vehículo
vehicle = connect('/dev/serial0', wait_ready=True, baud=115200)

# Crear o abrir el archivo de log
log_file = open('/home/pi/gps_log.txt', 'a')

# Función para tomar una foto y registrar la información del GPS
def tomar_foto_y_log(camera, vehicle):
    ret, frame = camera.read()
    if ret:
        # Obtener la información del GPS
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        alt = vehicle.location.global_frame.alt

        # Timestamp
        timestamp = int(time.time())

        # Guardar la imagen con timestamp
        filename = f"/home/pi/foto_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Foto guardada: {filename}")

        # Escribir en el log
        log_file.write(f"{timestamp}, {lat}, {lon}, {alt}\n")
        print(f"Log guardado: {timestamp}, {lat}, {lon}, {alt}")
    else:
        print("Error al capturar la imagen")

# Iniciar la cámara
camera = cv2.VideoCapture(0)  # Asegúrate de que el ID de la cámara es el correcto
time.sleep(2)  # Dar tiempo a que la cámara se inicie

# Esperar hasta que el vehículo esté listo para armar
while not vehicle.is_armable:
    print("Esperando que el vehículo esté listo para armar...")
    time.sleep(1)

# Cambiar a modo GUIDED (guiado)
vehicle.mode = VehicleMode("GUIDED")

# Armar el vehículo
vehicle.armed = True
while not vehicle.armed:
    print("Esperando para armar el vehículo...")
    time.sleep(1)

# Iniciar la misión preconfigurada
vehicle.commands.next = 0
vehicle.mode = VehicleMode("AUTO")
print("Iniciando misión...")

# Captura de fotos y log cada 2 segundos mientras se ejecuta la misión
while vehicle.commands.next < len(vehicle.commands):
    tomar_foto_y_log(camera, vehicle)
    time.sleep(2)  # Esperar 2 segundos entre cada foto

# Esperar hasta que la misión termine
while vehicle.mode.name == "AUTO" and vehicle.commands.next < len(vehicle.commands):
    print(f"Waypoint {vehicle.commands.next} de {len(vehicle.commands)}")
    time.sleep(1)

# Al finalizar la misión, cambiar a modo LOITER para mantener posición
vehicle.mode = VehicleMode("LOITER")
print("Misión completada, cambiando a modo LOITER...")

# Finalizar
camera.release()
log_file.close()
vehicle.close()
