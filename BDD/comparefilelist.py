def comparar_listas(ruta1, ruta2):
    try:
        # Leer archivos y limpiar espacios o saltos de línea
        with open(ruta1, 'r', encoding='utf-8') as f1, \
             open(ruta2, 'r', encoding='utf-8') as f2:
            
            # Convertimos a sets para una comparación instantánea
            set1 = set(line.strip() for line in f1 if line.strip())
            set2 = set(line.strip() for line in f2 if line.strip())

        # Diferencia simétrica: usuarios en A o en B, pero no en los dos
        unicos = set1 - set2

        if unicos:
            print(f"--- Se encontraron {len(unicos)} usuarios únicos ---")
            for usuario in sorted(unicos):
                # Opcional: Indicar de qué archivo viene
                origen = ruta1 if usuario in set1 else ruta2
                print(f"[Único en {origen}]: {usuario}")
        else:
            print("No hay diferencias. Ambas listas son idénticas.")

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo. {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- Configuración de rutas ---
archivo_a = r'C:\temp\instagram_data\uno_uniq.txt'
archivo_b = r'C:\temp\instagram_data\dos_uniq.txt'

comparar_listas(archivo_a, archivo_b)