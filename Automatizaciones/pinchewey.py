import os
import re

# Carpeta base donde están los archivos
BASE_DIR = r"A:\I+D\Desarrollo\Repositorios_Producto\FE-ArgentinaExterior-AppSource"  # <-- cambiar la ruta acá

# Regex para detectar ESP y ver si ESM ya existe
comment_pattern = re.compile(r"(Comment\s*=\s*'[^']*ESP=\"([^\"]+)\"[^']*')")

for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.lower().endswith(".al"):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Buscar comentarios con ESP y sin ESM
            def add_esm(match):
                full_comment = match.group(1)
                esp_value = match.group(2)
                if "ESM=" in full_comment:
                    return full_comment  # ya tiene ESM, no tocar
                else:
                    # Insertar antes del cierre de la comilla del comment
                    return full_comment[:-1] + f',ESM="{esp_value}"\''
            
            new_content = re.sub(comment_pattern, add_esm, content)

            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Actualizado: {file_path}")
            else:
                print(f"➡️ Sin cambios: {file_path}")

print("💥 Mi trabajo acá ha terminado! 💥")
