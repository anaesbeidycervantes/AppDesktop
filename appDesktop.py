import tkinter as tk
from tkinter import messagebox, ttk
import requests
import socket
import datetime


# Función para obtener la IP del cliente
def get_ip():
    hostname = socket.gethostname()  # Obtener el nombre del host
    return socket.gethostbyname(hostname)  # Obtener la dirección IP del host


# Función para agregar el registro
def add_car(action):
    name = name_entry.get()  # Obtener el nombre del usuario
    ip_client = get_ip()  # Obtener la IP automáticamente
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener la fecha y hora actual

    # Verificar que el campo de nombre no esté vacío
    if not name:
        messagebox.showerror("Error", "Por favor, completa el campo de nombre.")
        return

    # Crear el nuevo registro que se enviará
    new_car = {
        "status": action,
        "ipClient": ip_client,
        "name": name,
        "date": current_time  # Enviar la fecha y hora actuales
    }

    try:
        # Enviar el registro a la API local
        response = requests.post("http://127.0.0.1:5000/send_data", json=new_car)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        action_label.config(text=f"Acción enviada: {action} a las {current_time}")  # Actualizar la etiqueta
        print("Registro añadido:", response.json())  # Imprimir la respuesta del registro
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo añadir el registro: {e}")  # Mostrar error si ocurre


# Función para mostrar la ventana de registros
def show_records_window():
    records_frame.pack(fill=tk.BOTH, expand=True)  # Mostrar el marco de registros
    main_frame.pack_forget()  # Ocultar el marco principal

    try:
        # Obtener los registros de MockAPI
        response = requests.get("https://66eb042d55ad32cda47b5eb9.mockapi.io/IoTCarStatus")
        response.raise_for_status()
        records = response.json()

        # Limpiar la tabla
        for row in records_tree.get_children():
            records_tree.delete(row)

        # Insertar los últimos 10 registros en la tabla
        for record in records[-10:]:
            records_tree.insert("", tk.END, values=(
            record["id"], record["status"], record["name"], record["ipClient"], record["date"]))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudieron obtener los registros: {e}")


# Función para mostrar la ventana de acciones
def show_actions_window():
    main_frame.pack_forget()  # Ocultar el marco principal
    action_frame.pack()  # Mostrar el marco de acciones


# Función para volver a la ventana principal
def go_back():
    action_frame.pack_forget()  # Ocultar el marco de acciones
    records_frame.pack_forget()  # Ocultar el marco de registros
    main_frame.pack()  # Mostrar el marco principal


# Crear la ventana principal
app = tk.Tk()
app.title("Inyección de Registros")  # Título de la ventana

# Marco principal
main_frame = tk.Frame(app)
main_frame.pack(padx=10, pady=10)  # Empaquetar el marco principal

# Botones para registros y acciones
tk.Button(main_frame, text="Registros", command=show_records_window, width=20, height=2).pack(
    pady=5)  # Botón para registros
tk.Button(main_frame, text="Acciones", command=show_actions_window, width=20, height=2).pack(
    pady=5)  # Botón para acciones

# Marco de registros
records_frame = tk.Frame(app)
tk.Label(records_frame, text="Últimos 10 Registros", font=("Arial", 14)).pack(pady=5)  # Etiqueta de registros
records_tree = ttk.Treeview(records_frame, columns=("ID", "Estado", "Nombre", "IP Cliente", "Fecha"),
                            show='headings')  # Tabla para mostrar registros
records_tree.heading("ID", text="ID")  # Encabezado de ID
records_tree.heading("Estado", text="Estado")  # Encabezado de Estado
records_tree.heading("Nombre", text="Nombre")  # Encabezado de Nombre
records_tree.heading("IP Cliente", text="IP Cliente")  # Encabezado de IP Cliente
records_tree.heading("Fecha", text="Fecha")  # Encabezado de Fecha
records_tree.pack(padx=10, pady=10)  # Empaquetar la tabla

# Botón de regresar en la ventana de registros
tk.Button(records_frame, text="Regresar", command=go_back, width=20, height=2, bg="red").pack(
    pady=5)  # Botón para regresar a la ventana principal

# Marco de acciones
action_frame = tk.Frame(app)

# Etiquetas y entradas
tk.Label(action_frame, text="Nombre:").pack()  # Etiqueta para el nombre
name_entry = tk.Entry(action_frame, width=30)  # Campo de entrada para el nombre
name_entry.pack()

# Crear marco para los botones
button_frame = tk.Frame(action_frame)
button_frame.pack(pady=10)

# Botones para las acciones
actions = [
    "Adelante",
    "Atrás",
    "Vuelta a la derecha",
    "Vuelta a la izquierda",
    "Giro 90° a la derecha",
    "Giro 90° a la izquierda",
    "Detenerse",
    "Giro 360° a la derecha",
    "Giro 360° a la izquierda",
]

# Organizar botones en dos filas
for i, action_text in enumerate(actions):
    btn = tk.Button(button_frame, text=action_text, command=lambda a=action_text: add_car(a), width=20,
                    height=2)  # Botón para cada acción
    if i < 5:
        btn.pack(side=tk.TOP, padx=5)  # Primeros 5 botones en la parte superior
    else:
        btn.pack(side=tk.BOTTOM, padx=5)  # Últimos 4 botones en la parte inferior

# Botón de regresar a la ventana principal
tk.Button(action_frame, text="Atrás", command=go_back, width=20, height=2, bg="red").pack(
    pady=5)  # Botón para regresar a la ventana principal

# Etiqueta para mostrar la acción enviada
action_label = tk.Label(action_frame, text="", font=("Arial", 12))  # Etiqueta para mostrar el estado de la acción
action_label.pack()

# Ejecutar la aplicación
app.mainloop()  # Iniciar el bucle principal de la interfaz
