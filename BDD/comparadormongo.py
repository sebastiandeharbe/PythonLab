import pymongo
from datetime import datetime

def comparar_auditorias(target_user, db_uri="mongodb://localhost:27017/"):
    try:
        client = pymongo.MongoClient(db_uri)
        db = client["instagram"]
        collection = db["documento"]

        # 1. Obtener los últimos 2 registros ordenados por fecha (descendente)
        registros = list(collection.find({"usuario_auditado": target_user})
                         .sort("fecha_captura", -1)
                         .limit(2))

        if len(registros) < 2:
            print(f"Se necesitan al menos 2 capturas para comparar. Encontradas: {len(registros)}")
            return

        # El más reciente es el índice 0, el anterior es el índice 1
        actual = registros[0]
        anterior = registros[1]

        # Extraer listas de seguidores/seguidos
        # Usamos set() para poder hacer restas matemáticas de conjuntos
        seguidores_actual = set(actual["detalles"]["seguidores"])
        seguidores_anterior = set(anterior["detalles"]["seguidores"])
        
        seguidos_actual = set(actual["detalles"]["seguidos"])
        seguidos_anterior = set(anterior["detalles"]["seguidos"])

        print(f"--- Comparando {target_user} ---")
        print(f"Fecha Anterior: {anterior['fecha_captura'].strftime('%H:%M:%S')}")
        print(f"Fecha Actual:   {actual['fecha_captura'].strftime('%H:%M:%S')}")
        print("-" * 30)

        # 2. Análisis de SEGUIDORES (Gente que te sigue)
        nuevos_seguidores = seguidores_actual - seguidores_anterior
        unfollows_recibidos = seguidores_anterior - seguidores_actual

        if nuevos_seguidores:
            print(f"✅ Nuevos Seguidores ({len(nuevos_seguidores)}): {list(nuevos_seguidores)}")
        if unfollows_recibidos:
            print(f"❌ Te dejaron de seguir ({len(unfollows_recibidos)}): {list(unfollows_recibidos)}")

        # 3. Análisis de SEGUIDOS (Gente que vos seguís)
        nuevos_seguidos = seguidos_actual - seguidos_anterior
        seguidos_eliminados = seguidos_anterior - seguidos_actual

        if nuevos_seguidos:
            print(f"➕ Empezaste a seguir a ({len(nuevos_seguidos)}): {list(nuevos_seguidos)}")
        if seguidos_eliminados:
            print(f"➖ Dejaste de seguir a ({len(seguidos_eliminados)}): {list(seguidos_eliminados)}")

        if not (nuevos_seguidores or unfollows_recibidos or nuevos_seguidos or seguidos_eliminados):
            print("No hubo cambios entre estas dos capturas.")

    except Exception as e:
        print(f"Error en la comparación: {e}")

if __name__ == "__main__":
    # El usuario que usamos en el test de mock data
    comparar_auditorias("sebasdeharbe_test")