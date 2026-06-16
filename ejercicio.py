import csv
from datetime import datetime  # Necesario para registrar fecha y hora
import os

ARCHIVO = "usuarios.csv"
ARCHIVO_ERRORES = "errores.csv"  # Archivo solicitado para los datos corruptos


def registrar_usuario(usuarios):
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    nombre = input("Ingrese el nombre del usuario: ").strip()

    if nombre == "":
        print("Error: El nombre no puede estar vacío.")
        return

    if not all(c.isalpha() or c.isspace() for c in nombre):
        print("Error: El nombre solo debe contener letras.")
        return

    # NUEVO REQUERIMIENTO: Evitar usuarios duplicados en el momento del registro
    for u in usuarios:
        if u["nombre"].lower() == nombre.lower():
            print(f"Error: El usuario '{nombre}' ya existe en el sistema.")
            return

    try:
        edad = int(input("Ingrese la edad: "))

        # NUEVO REQUERIMIENTO: Registrar fecha y hora de creación
        # Formato resultante: "AAAA-MM-DD HH:MM:SS" (ej: 2026-06-10 21:30:15)
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        usuario = {
            "nombre": nombre.title(),
            "edad": edad,
            "fecha": fecha_registro,  # Se agrega al diccionario
        }

        usuarios.append(usuario)
        print("Usuario registrado en memoria temporal exitosamente.")

    except ValueError:
        print("Error: La edad debe ser un número entero.")


def mostrar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("No hay usuarios registrados en la sesión actual.")
        return

    print("\n--- USUARIOS EN MEMORIA ---")
    for i, usuario in enumerate(usuarios, start=1):
        # Mostramos también la fecha registrada
        print(
            f"{i}. Nombre: {usuario['nombre']} | Edad: {usuario['edad']} | Creado: {usuario['fecha']}"
        )


# NUEVO REQUERIMIENTO: Buscar usuarios por nombre
def buscar_usuario(usuarios):
    print("\n--- BUSCAR USUARIOS ---")
    if len(usuarios) == 0:
        print("No hay usuarios guardados para realizar una búsqueda.")
        return

    termino = (
        input("Ingrese el nombre (o parte de él) a buscar: ").strip().lower()
    )
    encontrados = []

    for usuario in usuarios:
        if termino in usuario["nombre"].lower():
            encontrados.append(usuario)

    if len(encontrados) == 0:
        print("No se encontraron usuarios que coincidan con la búsqueda.")
    else:
        print(f"\n--- Coincidencias encontradas ({len(encontrados)}) ---")
        for u in encontrados:
            print(f"• {u['nombre']} | Edad: {u['edad']} | Registro: {u['fecha']}")


# NUEVO REQUERIMIENTO: Validar un archivo al leerlo y separar datos buenos de malos
def validar_y_cargar_desde_archivo():
    usuarios_buenos = []
    errores_detectados = []

    if not os.path.exists(ARCHIVO):
        # Si el archivo no existe, devolvemos datos iniciales limpios por defecto
        print(
            f"El archivo '{ARCHIVO}' no existe. Iniciando con base de datos limpia."
        )
        return [
            {
                "nombre": "Carlos",
                "edad": 25,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            {
                "nombre": "Ana",
                "edad": 30,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        ]

    print(f"\n--- VALIDANDO Y LEYENDO ARCHIVO '{ARCHIVO}' ---")
    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if not fila:
                    continue  # Saltar líneas vacías

                # Estructura esperada en el CSV: nombre, edad, fecha
                nombre = fila[0].strip()
                edad_str = fila[1].strip()
                # Si el archivo viejo no tiene fecha, le asignamos la actual por defecto
                fecha = (
                    fila[2].strip()
                    if len(fila) > 2
                    else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                fila_con_error = False
                motivo_error = ""

                # Validaciones de la fila
                if nombre == "":
                    fila_con_error = True
                    motivo_error = "Nombre vacío"
                elif not all(c.isalpha() or c.isspace() for c in nombre):
                    fila_con_error = True
                    motivo_error = "Nombre contiene caracteres inválidos"

                try:
                    edad = int(edad_str)
                    if edad < 0 or edad > 120:
                        fila_con_error = True
                        motivo_error = "Edad fuera de rango (0-120)"
                except ValueError:
                    fila_con_error = True
                    motivo_error = "Edad no es un número entero"

                # Verificar duplicados en lo que ya se aceptó como bueno
                for u in usuarios_buenos:
                    if u["nombre"].lower() == nombre.lower():
                        fila_con_error = True
                        motivo_error = "Usuario duplicado en archivo"

                # Clasificación de datos
                if fila_con_error:
                    errores_detectados.append([nombre, edad_str, motivo_error])
                else:
                    usuarios_buenos.append(
                        {"nombre": nombre.title(), "edad": edad, "fecha": fecha}
                    )

        # Si se encontraron errores, creamos el archivo de errores separado
        if errores_detectados:
            print(
                f"⚠️ Se encontraron {len(errores_detectados)} filas corruptas."
            )
            with open(
                ARCHIVO_ERRORES, "w", newline="", encoding="utf-8"
            ) as archivo_err:
                escritor_err = csv.writer(archivo_err)
                # Guardamos: Nombre aportado, Edad aportada, Motivo del fallo
                escritor_err.writerows(errores_detectados)
            print(
                f"   -> Los datos corruptos se movieron a '{ARCHIVO_ERRORES}'."
            )
        else:
            print("✅ El archivo fue leído y no contenía ningún error.")

    except Exception as e:
        print(f"💥 Ocurrió un error al procesar el archivo: {e}")

    return usuarios_buenos


def guardar_csv(usuarios):
    if len(usuarios) == 0:
        print("No hay usuarios para guardar.")
        return

    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)

            # Guardamos los 3 campos: Nombre, Edad, FechaRegistro
            for usuario in usuarios:
                escritor.writerow(
                    [usuario["nombre"], usuario["edad"], usuario["fecha"]]
                )

        print(f"¡Excelente! Información guardada en '{ARCHIVO}' correctamente.")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")


def mostrar_menu():
    print("\n===== SISTEMA DE REGISTRO CSV =====")
    print("1. Registrar usuario (Memoria)")
    print("2. Mostrar usuarios en memoria")
    print("3. Buscar usuarios")
    print("4. Guardar información en CSV")
    print("5. Terminar el programa")


def ejecutar_programa():
    # MODIFICACIÓN: Al arrancar, lee el archivo, lo valida y separa lo bueno de lo malo
    usuarios = validar_y_cargar_desde_archivo()
    opcion = ""

    while opcion != "5":
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario(usuarios)
        elif opcion == "2":
            mostrar_usuarios(usuarios)
        elif opcion == "3":
            buscar_usuario(usuarios)
        elif opcion == "4":
            guardar_csv(usuarios)
        elif opcion == "5":
            print("Programa finalizado con éxito.")
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    ejecutar_programa()