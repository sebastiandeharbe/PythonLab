import re
import os
import shutil

def filtrar_tablas_modificadas(ruta_origen, sobrescribir_con_backup=False):
    """
    Filtra un archivo de objetos de Navision dejando únicamente los bloques
    OBJECT Table que tengan la propiedad Modified=Yes (o True).
    
    :param ruta_origen: Ruta del archivo TXT original.
    :param sobrescribir_con_backup: Si es True, guarda el archivo original como .bak 
                                   y reemplaza el original. Si es False, crea un archivo
                                   nuevo llamado '<nombre>_SoloTablasModificadas.txt'.
    """
    # Regex para identificar el inicio de un objeto
    regex_inicio_obj = re.compile(r"^OBJECT\s+([A-Za-z]+)\s+(\d+)", re.IGNORECASE)
    
    # Regex para detectar Modified=Yes o Modified=True en OBJECT-PROPERTIES
    regex_modificado = re.compile(r"Modified\s*=\s*(Yes|True)\s*;", re.IGNORECASE)

    # Definir ruta de salida provisional
    dir_nombre, archivo_nombre = os.path.split(ruta_origen)
    nombre_base, ext = os.path.splitext(archivo_nombre)
    ruta_salida = os.path.join(dir_nombre, f"{nombre_base}_SoloTablasModificadas{ext}")

    bloque_actual = []
    tipo_actual = None
    es_modificado = False
    en_propiedades = False
    tablas_guardadas = 0

    print(f"Procesando: {ruta_origen}...")

    with open(ruta_origen, "r", encoding="latin-1") as f_in, \
         open(ruta_salida, "w", encoding="latin-1") as f_out:

        def procesar_bloque():
            nonlocal tablas_guardadas
            # Solo guardamos si es Table y tiene Modified=Yes
            if tipo_actual and tipo_actual.lower() == "table" and es_modificado:
                f_out.writelines(bloque_actual)
                tablas_guardadas += 1

        for linea in f_in:
            match_obj = regex_inicio_obj.match(linea)
            if match_obj:
                # Si ya veníamos leyendo un objeto previo, evaluamos si correspondía guardarlo
                if bloque_actual:
                    procesar_bloque()

                # Reiniciamos variables para el nuevo objeto
                bloque_actual = [linea]
                tipo_actual = match_obj.group(1)
                es_modificado = False
                en_propiedades = False
                continue

            # Acumular la línea en el bloque del objeto en curso
            if bloque_actual:
                bloque_actual.append(linea)

                if "OBJECT-PROPERTIES" in linea:
                    en_propiedades = True
                    continue

                if en_propiedades:
                    if regex_modificado.search(linea):
                        es_modificado = True
                    elif linea.strip() == "}":
                        en_propiedades = False

        # Procesar el último objeto al llegar al final del archivo
        if bloque_actual:
            procesar_bloque()

    print(f"Proceso finalizado. Se conservaron {tablas_guardadas} tablas modificadas.")

    # Si se solicitó sobrescribir el archivo original
    if sobrescribir_con_backup:
        ruta_backup = os.path.join(dir_nombre, f"{nombre_base}.bak")
        shutil.copy2(ruta_origen, ruta_backup)
        shutil.move(ruta_salida, ruta_origen)
        print(f"Archivo original reemplazado: {ruta_origen}")
        print(f"Copia de respaldo creada en: {ruta_backup}")
    else:
        print(f"Nuevo archivo generado en: {ruta_salida}")


if __name__ == "__main__":
    # Configura aquí tus rutas
    archivo_txt = r"A:\Temp\VOXAWP\TodosObjVOXA.txt"

    # Si quieres que reemplace directamente el archivo origen (creando un .bak por seguridad), pon True.
    # Si prefieres dejar el original intacto y crear un archivo nuevo, déjalo en False.
    filtrar_tablas_modificadas(archivo_txt, sobrescribir_con_backup=False)