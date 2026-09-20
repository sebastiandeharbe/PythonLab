import sys
import os

def procesar_usuarios(ruta_origen, ruta_destino):
    if not os.path.exists(ruta_origen):
        print(f"Error: El archivo '{ruta_origen}' no existe.")
        return

    # Usamos un set para eliminar duplicados y strip para limpiar espacios
    with open(ruta_origen, 'r', encoding='utf-8') as f:
        # El uso de set() garantiza unicidad
        usuarios = {linea.strip() for linea in f if linea.strip()}

    # Escribimos el resultado ordenado alfabéticamente
    with open(ruta_destino, 'w', encoding='utf-8') as f:
        for usuario in sorted(usuarios):
            f.write(f"{usuario}\n")

    print(f"Proceso completado. Usuarios únicos guardados en: {ruta_destino}")

if __name__ == "__main__":
    # Verificamos que se pasen los argumentos necesarios
    if len(sys.argv) < 3:
        print("Uso: python script.py <ruta_origen> <ruta_destino>")
    else:
        procesar_usuarios(sys.argv[1], sys.argv[2])