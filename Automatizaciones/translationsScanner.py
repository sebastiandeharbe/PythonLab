import os
import re

# Regex
caption_regex = re.compile(r'Caption\s*=\s*\'[^\']*\'', re.IGNORECASE)
label_regex = re.compile(r'\w+\s*:\s*Label\s*\'[^\']*\'', re.IGNORECASE)
comment_regex = re.compile(r'Comment\s*=\s*\'[^\']*ESP\s*=\s*".*?"[^\']*\'', re.IGNORECASE)


def es_archivo_al(nombre_archivo):
    # Solo archivos que TERMINAN exactamente en .al (case insensitive)
    return nombre_archivo.lower().endswith('.al')


def analizar_archivo(ruta_archivo):
    problemas = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        if caption_regex.search(linea) or label_regex.search(linea):
            tiene_comment = False

            # Revisar bloque (línea actual + 3 siguientes)
            for j in range(i, min(i + 4, len(lineas))):
                if comment_regex.search(lineas[j]):
                    tiene_comment = True
                    break

            if not tiene_comment:
                problemas.append((i + 1, linea))

        i += 1

    return problemas


def recorrer_directorio(directorio):
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if es_archivo_al(file):  # 👈 filtro estricto
                ruta_completa = os.path.join(root, file)
                problemas = analizar_archivo(ruta_completa)

                if problemas:
                    print(f"\n📄 Archivo: {ruta_completa}")
                    for linea_num, contenido in problemas:
                        print(f"  ❌ Línea {linea_num}: {contenido}")


if __name__ == "__main__":
    ruta_proyecto = r"A:\I+D\Desarrollo\Clientes\DVA Argentina\DVA Argentina - Personalizaciones"
    recorrer_directorio(ruta_proyecto)