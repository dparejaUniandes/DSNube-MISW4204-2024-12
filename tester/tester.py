import subprocess
import json
import csv
import os
import requests

# Configuración de las pruebas de carga
signup_url = "http://localhost:81/user/api/auth/signup"
login_url = "http://localhost:81/user/api/auth/login"
tasks_url = "http://localhost:81/user/api/tasks"

signup_data_file = "signup_data.json"
login_data_file = "login_data.json"
video_file = "video.mp4"

scenarios = [
  {"requests": 10, "concurrency": 10},
  {"requests": 50, "concurrency": 50},
  {"requests": 100, "concurrency": 100},
  {"requests": 200, "concurrency": 200},
  {"requests": 300, "concurrency": 300},
  {"requests": 400, "concurrency": 400}
]

# Leer los datos JSON desde los archivos
with open(signup_data_file, "r") as file:
  signup_data = json.load(file)

with open(login_data_file, "r") as file:
  login_data = json.load(file)

# Función para obtener el token de autorización
def get_auth_token():
  response = requests.post(login_url, json=login_data)
  if response.status_code == 200:
    data = response.json()
    return data["token"]
  else:
    raise Exception("Failed to obtain auth token")

# Función para ejecutar las pruebas de carga con Apache Benchmark
def run_load_test(url, requests, concurrency, data_file=None, header=None):
  command = f"ab -n {requests} -c {concurrency}"
  if data_file:
    command += f" -p {data_file}"
  if header:
    command += f' -H "{header}"'
  command += f" {url}"
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, error = process.communicate()
  return output.decode("utf-8"), error.decode("utf-8")

def extract_values(output):
  lines = output.split("\n")
  requests_per_second = next((line.split(":")[1].strip() for line in lines if "Requests per second" in line), "")
  time_per_request = next((line.split(":")[1].strip() for line in lines if "Time per request" in line and "mean" in line), "")
  transfer_rate = next((line.split(":")[1].strip() for line in lines if "Transfer rate" in line), "")
  return requests_per_second, time_per_request, transfer_rate

def save_results_to_csv(results):
  endpoints = ["registro", "inicio_de_sesion", "carga_de_video"]
  
  for endpoint in endpoints:
    file_name = f"load_test_results_{endpoint}.csv"
    
    with open(file_name, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["Requests", "Concurrency", "Requests per second", "Time per request (ms)", "Transfer rate (kb/s)"])
      
      for result in results:
        if result["endpoint"] == endpoint:
          requests = result["requests"]
          concurrency = result["concurrency"]
          output = result["output"]
          
          requests_per_second, time_per_request, transfer_rate = extract_values(output)
          
          writer.writerow([requests, concurrency, requests_per_second, time_per_request, transfer_rate])

# Obtener el token de autorización
auth_token = get_auth_token()

# Lista y diccionario para almacenar los resultados de las pruebas de carga
load_test_results = []

# Ejecutar las pruebas de carga para cada escenario
for scenario in scenarios:
  requests = scenario["requests"]
  concurrency = scenario["concurrency"]

  # Prueba de carga - registro de usuarios
  print(f"Ejecutando prueba de carga para el registro de usuarios con {requests} solicitudes y {concurrency} de concurrencia...")
  output, error = run_load_test(signup_url, requests, concurrency, signup_data_file)
  print("Resultado:")
  print(output)
  print("Error (si hay alguno):")
  print(error)
  print("---")
  load_test_results.append({"endpoint": "registro", "requests": requests, "concurrency": concurrency, "output": output})

  # Prueba de carga - inicio de sesion
  print(f"Ejecutando prueba de carga para el inicio de sesion con {requests} solicitudes y {concurrency} de concurrencia...")
  output, error = run_load_test(login_url, requests, concurrency, login_data_file)
  print("Resultado:")
  print(output)
  print("Error (si hay alguno):")
  print(error)
  print("---")
  load_test_results.append({"endpoint": "inicio_de_sesion", "requests": requests, "concurrency": concurrency, "output": output})

  # Prueba de carga - carga de video
  print(f"Ejecutando prueba de carga para la carga de video con {requests} solicitudes y {concurrency} de concurrencia...")
  header = f'Authorization: Bearer {auth_token}'
  output, error = run_load_test(tasks_url, requests, concurrency, header=header, data_file=video_file)
  print("Resultado:")
  print(output)
  print("Error (si hay alguno):")
  print(error)
  print("---")
  load_test_results.append({"endpoint": "carga_de_video", "requests": requests, "concurrency": concurrency, "output": output})

# Guardar los resultados
save_results_to_csv(load_test_results)

print("Los resultados de las pruebas de carga se han guardado en archivo csv.")