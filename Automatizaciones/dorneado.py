import os
import shutil

# Ruta a la carpeta que contiene los archivos .al
carpeta = r"A:\Temp\20251202-WeFIV\WeFIV-AL"  # <-- cámbiala por la tuya

for archivo in os.listdir(carpeta):
    if archivo.endswith(".al") and "." in archivo:
        partes = archivo.split(".")
        if len(partes) >= 3:
            tipo = partes[-2]  # la parte antes de ".al"
            subcarpeta = os.path.join(carpeta, tipo)

            # Crear la subcarpeta si no existe
            os.makedirs(subcarpeta, exist_ok=True)

            # Mover el archivo
            origen = os.path.join(carpeta, archivo)
            destino = os.path.join(subcarpeta, archivo)
            shutil.move(origen, destino)
            print(f"Movido: {archivo} -> {tipo}/")

print("Archivos ordenados por tipo. ✅")