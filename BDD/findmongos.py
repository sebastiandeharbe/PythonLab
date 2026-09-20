import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Listar todas las DBs
print("Bases de datos encontradas:")
for db_name in client.list_database_names():
    print(f"-> DB: {db_name}")
    db = client[db_name]
    for coll_name in db.list_collection_names():
        count = db[coll_name].count_documents({})
        print(f"   - Colección: {coll_name} ({count} documentos)")