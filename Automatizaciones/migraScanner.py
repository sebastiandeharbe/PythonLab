import os
import csv
import re

# Configuración
PROYECTO_AL_PATH = r'A:\I+D\Desarrollo\Clientes\DVA Argentina\DVA Argentina - Personalizaciones'  # <-- CAMBIA ESTO POR TU RUTA
ARCHIVO_CSV_PATH = r'A:\Temp\20251215-AGM\ObjetosModNAV.csv'   # <-- CAMBIA ESTO POR TU RUTA

# Mapeo de tipos NAV a tipos AL
TYPE_MAPPING = {
    'Table': {'base': 'table', 'ext': 'tableextension'},
    'Page': {'base': 'page', 'ext': 'pageextension'},
    'Codeunit': {'base': 'codeunit', 'ext': None},
    'Query': {'base': 'query', 'ext': None},
    'Report': {'base': 'report', 'ext': 'reportextension'},
    'XmlPort': {'base': 'xmlport', 'ext': None},
    'Enum': {'base': 'enum', 'ext': 'enumextension'},
}

def clean_name(name):
    """Limpia comillas y espacios para normalizar comparaciones"""
    if not name: return ""
    return name.strip().replace('"', '').lower()

def scan_al_project(folder_path):
    """
    Escanea la carpeta recursivamente y devuelve dos diccionarios:
    1. objects_by_id: { ('table', '3'): True, ... }
    2. extensions_by_target: { ('table', 'payment terms'): True, ... }
    """
    print(f"--- Escaneando proyecto AL en: {folder_path} ---")
    
    objects_by_id = set()
    extensions_by_target = set()

    # Regex para detectar objetos base: ej: table 50100 "My Table"
    # Grupo 1: Tipo, Grupo 2: ID
    regex_obj = re.compile(r'^\s*(table|page|codeunit|report|query|xmlport|enum)\s+(\d+)', re.IGNORECASE | re.MULTILINE)

    # Regex para detectar extensiones: ej: tableextension 50100 MyExt extends "Payment Terms"
    # Grupo 1: Tipo (tableextension), Grupo 4: Nombre del objeto base (Payment Terms)
    regex_ext = re.compile(r'^\s*(tableextension|pageextension|reportextension|enumextension)\s+(\d+)\s+(?:"?.*?"?)\s+extends\s+"?(.+?)"?(?:\s|//|{|$)', re.IGNORECASE | re.MULTILINE)

    count_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.al'):
                count_files += 1
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                        content = f.read()
                        
                        # Buscar objetos base
                        match_obj = regex_obj.search(content)
                        if match_obj:
                            obj_type = match_obj.group(1).lower()
                            obj_id = match_obj.group(2)
                            objects_by_id.add((obj_type, obj_id))

                        # Buscar extensiones
                        match_ext = regex_ext.search(content)
                        if match_ext:
                            ext_type = match_ext.group(1).lower()
                            # Limpiamos el nombre del objeto extendido (target)
                            target_name = clean_name(match_ext.group(3))
                            
                            # Mapeamos 'tableextension' a 'table' para facilitar la búsqueda inversa
                            base_type = ext_type.replace('extension', '')
                            extensions_by_target.add((base_type, target_name))

                except Exception as e:
                    print(f"Error leyendo {file}: {e}")

    print(f"--- Escaneo completo. Archivos AL analizados: {count_files} ---")
    return objects_by_id, extensions_by_target

def check_csv(csv_path, found_ids, found_exts):
    print(f"\n--- Analizando CSV: {csv_path} ---")
    print("OBJETOS FALTANTES:\n")
    
    missing_count = 0
    
    try:
        with open(csv_path, 'r', encoding='latin-1') as csvfile: # NAV suele exportar en latin-1 o ansi
            # El delimitador es punto y coma según tu ejemplo
            reader = csv.reader(csvfile, delimiter=';')
            
            for row in reader:
                if not row or len(row) < 3: continue
                
                # Parsear línea del CSV
                nav_type = row[0].strip()   # Ej: Table
                nav_id = row[1].strip()     # Ej: 3
                nav_name = row[2].strip()   # Ej: Payment Terms
                
                # Ignorar encabezados si los hay (detectando si el ID no es numérico)
                if not nav_id.isdigit(): continue

                # Normalizar para búsqueda
                search_type = nav_type.lower()
                clean_nav_name = clean_name(nav_name)
                
                # Mapear tipos especiales (ej: Country/Region en NAV puede ser confuso, pero el tipo base es Table)
                # Asumimos que el tipo en CSV coincide con el tipo base en AL
                
                found = False
                
                # ESTRATEGIA 1: Buscar por ID (Objeto Custom o Base redefinido)
                # Verifica si existe 'table 3' o 'table 50000'
                if (search_type, nav_id) in found_ids:
                    found = True
                
                # ESTRATEGIA 2: Buscar por Extensión (Standard extendido)
                # Si es Table, busca si existe tableextension que extienda "Payment Terms"
                if not found and nav_type in TYPE_MAPPING:
                    ext_suffix = TYPE_MAPPING[nav_type]['extension']
                    if ext_suffix:
                        # Buscamos en el set de extensiones usando el nombre
                        if (search_type, clean_nav_name) in found_exts:
                            found = True

                # Resultado
                if not found:
                    missing_count += 1
                    # Formato de salida para consola
                    print(f"[FALTA] Tipo: {nav_type:<10} ID: {nav_id:<6} Nombre: {nav_name}")

    except Exception as e:
        print(f"Error procesando CSV: {e}")
    
    if missing_count == 0:
        print("\n¡Todo correcto! Se encontraron todos los objetos del CSV en el proyecto AL.")
    else:
        print(f"\nTotal de objetos faltantes: {missing_count}")

if __name__ == "__main__":
    if os.path.exists(PROYECTO_AL_PATH) and os.path.exists(ARCHIVO_CSV_PATH):
        # 1. Escanear lo que tenemos
        ids_encontrados, extensiones_encontradas = scan_al_project(PROYECTO_AL_PATH)
        
        # 2. Verificar contra lo que queremos
        check_csv(ARCHIVO_CSV_PATH, ids_encontrados, extensiones_encontradas)
    else:
        print("Error: Verifica las rutas del proyecto AL y el archivo CSV.")