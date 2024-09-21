from flask import Flask, jsonify, request
import requests
import datetime

# Inicialización de la aplicación Flask
app = Flask(__name__)

# URL base de la API externa
base_url = "https://66eb042d55ad32cda47b5eb9.mockapi.io/IoTCarStatus"

# Ruta para inyectar registros a MockAPI (POST)
@app.route('/send_data', methods=['POST'])
def create_car():
    try:
        new_car = request.json  # Obtenemos el contenido del cuerpo de la solicitud en formato JSON

        # Validamos y creamos un objeto con los datos esperados
        car_data = {
            'status': new_car.get('status', 'Unknown'),
            'date': str(datetime.datetime.now().date()),  # Fecha actual
            'time': str(datetime.datetime.now().time()),  # Hora actual
            'ipClient': new_car.get('ipClient', '0.0.0.0'),  # Dirección IP por defecto
            'name': new_car.get('name', 'Anonymous')  # Nombre por defecto si no se proporciona
        }

        response = requests.post(base_url, json=car_data)
        response.raise_for_status()  # Verifica que la respuesta sea exitosa
        created_car = response.json()
        return jsonify(created_car), 201  # Devolvemos el auto creado con el código 201 (creado)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ruta para obtener todos los registros (GET)
@app.route('/send_data', methods=['GET'])
def get_cars():
    try:
        # Realizamos una solicitud GET a la API externa
        response = requests.get(base_url)
        response.raise_for_status()  # Verifica que la respuesta sea exitosa
        cars = response.json()  # Parseamos la respuesta en formato JSON
        return jsonify(cars), 200  # Devolvemos la lista de autos
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
