import csv
from datetime import datetime  # Necesario para registrar fecha y hora
import os


def validar_linea_usuario(fila, num_linea, usuarios_buenos):
    if len(fila) < 2:
        contenido_crudo = "".join(fila) if fila else "[Linea Vacia]"
        return False, f"Estructura invalida (Faltan campos o comas en linea {num_linea})"

    nombre = fila[0].strip()
    edad_str = fila[1].strip()

    if nombre == "":
        return False, "Nombre vacio"
    
    if not all(c.isalpha() or c.isspace() for c in nombre):
        return False, "Nombre contiene caracteres invalidos (numeros o simbolos)"

    try:
        edad = int(edad_str)
        if edad < 0 or edad > 120:
            return False, f"Edad fuera de rango (0-120): {edad_str}"
    except ValueError:
        return False, f"Edad no es un numero entero: '{edad_str}'"

    for u in usuarios_buenos:
        if u["nombre"].lower() == nombre.lower():
            return False, f"Usuario duplicado: '{nombre}' ya existe en la lista"

    fecha = (
        fila[2].strip()
        if len(fila) > 2
        else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    usuario = {
        "nombre": nombre.title(),
        "edad": edad,
        "fecha": fecha
    }
    return True, usuario


def registrar_usuario(usuarios):
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    nombre = input("Ingrese el nombre del usuario: ").strip()

    if nombre == "":
        print("Error: El nombre no puede estar vacío.")
        return

    if not all(c.isalpha() or c.isspace() for c in nombre):
        print("Error: El nombre solo debe contener letras.")
        return

    for u in usuarios:
        if u["nombre"].lower() == nombre.lower():
            print(f"Error: El usuario '{nombre}' ya existe en el sistema.")
            return

    try:
        edad = int(input("Ingrese la edad: "))
        if edad < 0 or edad > 120:
            print("Error: La edad debe estar en un rango logico (0-120).")
            return

        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        usuario = {
            "nombre": nombre.title(),
            "edad": edad,
            "fecha": fecha_registro,
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
        print(
            f"{i}. Nombre: {usuario['nombre']:<15} | Edad: {usuario['edad']:<3} | Creado: {usuario['fecha']}"
        )


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


def gestionar_memoria(usuarios):
    """
    Submenu para ordenar o eliminar registros activos en la memoria.
    """
    if len(usuarios) == 0:
        print("\nNo hay usuarios en memoria para modificar u ordenar.")
        return

    print("\n--- GESTIONAR MEMORIA (ORDENAR / ELIMINAR) ---")
    print("1. Ordenar usuarios por edad (Menor a Mayor)")
    print("2. Ordenar usuarios por edad (Mayor a Menor)")
    print("3. Eliminar un usuario por nombre exacto")
    print("4. Volver al menú principal")
    
    subopcion = input("Seleccione una opción de gestión: ").strip()

    if subopcion == "1":
        usuarios.sort(key=lambda x: x["edad"])
        print("Usuarios ordenados por edad de menor a mayor con éxito. Usa la opción 2 para verlos.")
        
    elif subopcion == "2":
        usuarios.sort(key=lambda x: x["edad"], reverse=True)
        print("Usuarios ordenados por edad de mayor a menor con éxito. Usa la opción 2 para verlos.")
        
    elif subopcion == "3":
        nombre_eliminar = input("Ingrese el nombre exacto del usuario a eliminar: ").strip().lower()
        inicial_len = len(usuarios)
        
        # Filtrado defensivo: mantiene solo los que NO coinciden con el nombre ingresado
        usuarios[:] = [u for u in usuarios if u["nombre"].lower() != nombre_eliminar]
        
        # CORREGIDO: Se unifico el nombre de la variable de control a 'inicial_len'
        if len(usuarios) < inicial_len:
            print(f"Eliminación exitosa: El usuario fue removido de la memoria actual.")
        else:
            print("No se encontró ningún usuario con ese nombre exacto.")
            
    elif subopcion == "4":
        return
    else:
        print("Opción inválida en el submenú.")


def calcular_edad_promedio(usuarios):
    """
    NUEVA FUNCIÓN: Calcula y muestra la media aritmética de las edades 
    de los usuarios cargados actualmente en memoria.
    """
    print("\n--- CALCULAR EDAD PROMEDIO ---")
    if len(usuarios) == 0:
        print("No hay usuarios en memoria para realizar el cálculo.")
        return

    # Sumatoria de todas las edades acumuladas
    suma_edades = sum(u["edad"] for u in usuarios)
    total_usuarios = len(usuarios)
    promedio = suma_edades / total_usuarios

    print(f"Estadísticas actuales:")
    print(f"  • Total de usuarios analizados: {total_usuarios}")
    print(f"  • Edad promedio: {promedio:.2f} años")


def cargar_y_segregar_archivo(usuarios_actuales):
    """
    Carga un archivo, aplica la validacion defensiva y escribe de forma
    inmediata dos archivos basados en el nombre original: _correctos y _errores.
    """
    print("\n--- CARGAR Y VALIDAR ARCHIVO EXTERNO ---")
    nombre_archivo = input("Ingrese el nombre o ruta del archivo .txt a cargar: ").strip()

    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo '{nombre_archivo}' no existe en el directorio.")
        return

    nombre_base, extension = os.path.splitext(nombre_archivo)
    ruta_correctos = f"{nombre_base}_correctos{extension}"
    ruta_errores = f"{nombre_base}_errores{extension}"

    usuarios_buenos_carga = []
    errores_detectados = []

    print(f"\n--- PROCESANDO Y AUDITANDO: '{nombre_archivo}' ---")
    try:
        with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for num_linea, fila in enumerate(lector, start=1):
                if not fila or len(fila) == 0 or (len(fila) == 1 and fila[0].strip() == ""):
                    continue 

                es_valido, resultado = validar_linea_usuario(fila, num_linea, usuarios_buenos_carga)

                if es_valido:
                    usuarios_buenos_carga.append(resultado)
                else:
                    nombre_error = fila[0].strip() if len(fila) > 0 else "[Vacio]"
                    edad_error = fila[1].strip() if len(fila) > 1 else "N/A"
                    errores_detectados.append([nombre_error, edad_error, resultado])

        if usuarios_buenos_carga:
            with open(ruta_correctos, "w", newline="", encoding="utf-8") as archivo_corr:
                escritor_corr = csv.writer(archivo_corr)
                for u in usuarios_buenos_carga:
                    escritor_corr.writerow([u["nombre"], u["edad"], u["fecha"]])
            print(f"Registros validos guardados en: '{ruta_correctos}' ({len(usuarios_buenos_carga)} usuarios)")
            
            usuarios_actuales.extend(usuarios_buenos_carga)
        else:
            print("Info: No se encontraron registros validos para exportar.")

        if errores_detectados:
            with open(ruta_errores, "w", newline="", encoding="utf-8") as archivo_err:
                escritor_err = csv.writer(archivo_err)
                escritor_err.writerow(["Nombre Aportado", "Edad Aportada", "Motivo del Fallo"])
                escritor_err.writerows(errores_detectados)
            print(f"Registros corruptos aislados en: '{ruta_errores}' ({len(errores_detectados)} errores)")
        else:
            print("Confirmacion: Cero inconsistencias detectadas en este archivo.")

    except PermissionError:
        print(f"Error: Permisos insuficientes para leer o escribir los archivos de auditoria.")
    except Exception as e:
        print(f"Ocurrio un error inesperado al segregar los datos: {e}")


def guardar_txt(usuarios):
    if len(usuarios) == 0:
        print("No hay usuarios para guardar.")
        return

    nombre_salida = input("Ingrese el nombre del archivo para exportar la memoria actual (ej: copia.txt): ").strip()
    if nombre_salida == "":
        print("Error: El nombre del archivo no puede estar vacío.")
        return

    try:
        with open(nombre_salida, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            for usuario in usuarios:
                escritor.writerow([usuario["nombre"], usuario["edad"], usuario["fecha"]])

        print(f"¡Excelente! Información exportada en '{nombre_salida}' correctamente.")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")


def mostrar_menu():
    print("\n===== SISTEMA DE GESTIÓN Y AUDITORÍA DE ARCHIVOS TXT =====")
    print("1. Registrar usuario manualmente (Memoria)")
    print("2. Mostrar usuarios en memoria")
    print("3. Buscar usuarios")
    print("4. Ordenar o Eliminar usuarios (Memoria)")
    print("5. Calcular la edad promedio de los usuarios (NUEVO)")
    print("6. Cargar y validar archivo (.txt)")
    print("7. Exportar memoria actual a un archivo personalizado")
    print("8. Terminar el programa")


def ejecutar_programa():
    usuarios = []
    opcion = ""

    while opcion != "8":
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario(usuarios)
        elif opcion == "2":
            mostrar_usuarios(usuarios)
        elif opcion == "3":
            buscar_usuario(usuarios)
        elif opcion == "4":
            gestionar_memoria(usuarios)
        elif opcion == "5":
            calcular_edad_promedio(usuarios)
        elif opcion == "6":
            cargar_y_segregar_archivo(usuarios)
        elif opcion == "7":
            get_nombre = guardar_txt(usuarios)
        elif opcion == "8":
            print("Programa finalizado con éxito.")
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    ejecutar_programa()