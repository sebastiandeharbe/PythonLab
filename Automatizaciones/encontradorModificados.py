import re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def exportar_objetos_modificados_excel(ruta_archivo_txt, ruta_salida_excel=r"A:\Temp\VOXAWARP\ObjetosModificados.xlsx"):
    regex_objeto = re.compile(r"^OBJECT\s+([A-Za-z]+)\s+(\d+)", re.IGNORECASE)
    regex_modificado = re.compile(r"Modified\s*=\s*Yes\s*;", re.IGNORECASE)

    objeto_actual = None
    en_propiedades = False
    objetos_modificados = []

    print("Leyendo archivo de Navision...")
    with open(ruta_archivo_txt, "r", encoding="latin-1") as archivo:
        for linea in archivo:
            match_obj = regex_objeto.match(linea)
            if match_obj:
                tipo, obj_id = match_obj.groups()
                objeto_actual = (tipo.capitalize(), int(obj_id))
                en_propiedades = False
                continue

            if "OBJECT-PROPERTIES" in linea:
                en_propiedades = True
                continue

            if en_propiedades and regex_modificado.search(linea):
                if objeto_actual:
                    objetos_modificados.append(objeto_actual)
                en_propiedades = False

            if en_propiedades and linea.strip() == "}":
                en_propiedades = False

    print(f"Total de objetos modificados encontrados: {len(objetos_modificados)}")

    # Crear el libro de Excel con formato profesional
    wb = Workbook()
    ws = wb.active
    ws.title = "Objetos Modificados"

    # Encabezados
    headers = ["TIPO", "ID"]
    ws.append(headers)

    # Estilos para encabezados
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")  # Azul oscuro profesional
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )

    for col_idx, _ in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if col_idx == 2 else "left", vertical="center")

    # Insertar filas
    for row_idx, (tipo, obj_id) in enumerate(objetos_modificados, start=2):
        ws.append([tipo, obj_id])
        
        # Formato de celdas de datos
        c_tipo = ws.cell(row=row_idx, column=1)
        c_id = ws.cell(row=row_idx, column=2)

        c_tipo.alignment = Alignment(horizontal="left", vertical="center")
        c_id.alignment = Alignment(horizontal="right", vertical="center")
        c_id.number_format = '#,##0'  # Formato numérico

        c_tipo.border = thin_border
        c_id.border = thin_border

    # Ajustar ancho de columnas automáticamente y habilitar filtros
    ws.column_dimensions['A'].width = 18
    ws.column_dimensions['B'].width = 14
    ws.auto_filter.ref = ws.dimensions

    # Guardar
    wb.save(ruta_salida_excel)
    print(f"Archivo Excel generado con éxito en: {ruta_salida_excel}")


if __name__ == "__main__":
    # Recuerda usar r"..." para las rutas de Windows
    ruta_txt = r"A:\Temp\VOXAWP\TodosObjVOXA.txt"
    ruta_excel = r"A:\Temp\VOXAWP\ObjetosModificados.xlsx"

    exportar_objetos_modificados_excel(ruta_txt, ruta_excel)
