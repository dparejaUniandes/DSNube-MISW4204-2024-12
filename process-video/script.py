import cv2
import time

start_time = time.time()

# Ruta del video de entrada
video_path = 'video.mp4'

# Ruta del logo
logo_path = 'logo.png'

try:
  # Cargar el video
  video = cv2.VideoCapture(video_path)

  # Cargar el logo
  logo = cv2.imread(logo_path)

  # Obtener las propiedades del video
  fps = video.get(cv2.CAP_PROP_FPS)
  width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # Calcular el nuevo ancho y alto para una relación de aspecto de 16:9
  new_width = width
  new_height = int(width * 9 / 16)

  # Calcular los márgenes superior e inferior para centrar el video
  top_margin = int((height - new_height) / 2)
  bottom_margin = height - new_height - top_margin

  # Redimensionar el logo al tamaño del video recortado
  logo = cv2.resize(logo, (new_width, new_height))

  # Crear el objeto de escritura de video
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  output_video = cv2.VideoWriter('video_recortado.mp4', fourcc, fps, (new_width, new_height))

  # Calcular la duración máxima en frames (20 segundos)
  max_duration = int(fps * 20)

  # Procesar el video
  output_video.write(logo)
  frame_count = 0
  while frame_count < max_duration:
    ret, frame = video.read()
    if not ret:
      break

    # Recortar el video a la relación de aspecto de 16:9
    cropped_frame = frame[top_margin:top_margin+new_height, :]

    # Escribir el frame en el video de salida
    output_video.write(cropped_frame)

    frame_count += 1
  output_video.write(logo)

finally:
  # Liberar los recursos
  video.release()
  output_video.release()
  cv2.destroyAllWindows()

end_time = time.time()  # Tiempo de finalización
execution_time = end_time - start_time  # Tiempo de ejecución

print("¡Proceso completado!")
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")