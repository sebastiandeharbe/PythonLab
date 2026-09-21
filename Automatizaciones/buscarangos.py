import json
from pathlib import Path

# Cambia esta ruta a la carpeta raíz de tus proyectos
ROOT_DIR = Path(r"A:\SAD\VOXA-SA_GitHub")


def obtener_rangos_al(ruta_base: Path):
    apps_encontradas = []

    # Busca recursivamente todos los archivos app.json
    for app_file in ruta_base.rglob("app.json"):
        try:
            with open(app_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)

            app_name = data.get("name", app_file.parent.name)

            # Soporta idRanges (múltiples) o idRange (único legacy)
            ranges = data.get("idRanges", [])
            if not ranges and "idRange" in data:
                ranges = [data["idRange"]]

            for r in ranges:
                r_from = r.get("from")
                r_to = r.get("to")

                if r_from is not None and r_to is not None:
                    apps_encontradas.append({
                        "name": app_name,
                        "from": int(r_from),
                        "to": int(r_to),
                        "path": str(app_file)
                    })

        except (json.JSONDecodeError, OSError) as e:
            print(f"[Aviso] No se pudo leer {app_file}: {e}")

    # Ordenar por 'from' ascendente (y 'to' como criterio secundario)
    apps_encontradas.sort(key=lambda x: (x["from"], x["to"]))
    return apps_encontradas


if __name__ == "__main__":
    lista_apps = obtener_rangos_al(ROOT_DIR)

    # Imprimir en consola con formato de tabla
    header = f"{'Nombre App':<40} | {'Desde':<10} | {'Hasta':<10}"
    print(header)
    print("-" * len(header))

    for item in lista_apps:
        print(f"{item['name']:<40} | {item['from']:<10} | {item['to']:<10}")