import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from models.restaurant import Restaurant

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Dados dos restaurantes do TripAdvisor
RESTAURANT_DATA = [
    {
        "name": "Pousada Bar e Restaurante Farol das Estrelas",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxyZXN0YXVyYW50fGVufDB8fHx8MTc1NzQ0MTgwMnww&ixlib=rb-4.1.0&q=85",
        "instagram": "@faroldasestrelasoficial",
        "hasPool": False,
        "hours": "Conforme temporada - consulte disponibilidade",
        "phones": ["(91) 99188-2030"],
        "categories": ["restaurants", "hospedagem"],
        "location": "3.6 km de Cotijuba",
        "comments": "1 avaliação",
        "rating": 4.0,
        "cuisine": "Brasileira, Frutos do mar"
    },
    {
        "name": "Na Telha",
        "image": "https://images.unsplash.com/photo-1620898670223-6f7f07d82a3b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxlY28lMjB0b3VyaXNtfGVufDB8fHx8MTc1NzQ0MTgxMHww&ixlib=rb-4.1.0&q=85",
        "instagram": "@natelhabelm",
        "hasPool": False,
        "hours": "Almoço - das 11h às 15h (fecha em breve)",
        "phones": ["(91) 99315-4021"],
        "categories": ["restaurants", "rio-guama"],
        "location": "9.2 km - Rio Guamá",
        "comments": "142 avaliações",
        "rating": 4.2,
        "cuisine": "Brasileira, Frutos do mar"
    },
    {
        "name": "Mr. Brasa Gastronomia E Entretenimento",
        "image": "https://images.unsplash.com/photo-1591081658714-f576fb7ea3ed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxhbWF6b24lMjByaXZlcnxlbnwwfHx8fDE3NTc0NDE3Njh8MA&ixlib=rb-4.1.0&q=85",
        "instagram": "@mrbrasabelem",
        "hasPool": False,
        "hours": "Aberto agora - das 18h às 02h",
        "phones": ["(91) 99383-7451"],
        "categories": ["restaurants", "igarape-combu"],
        "location": "9.1 km - Icoaraci",
        "comments": "14 avaliações",
        "rating": 3.9,
        "cuisine": "Brasileira, Sul-americana"
    },
    {
        "name": "Resto Da Vila",
        "image": "https://images.unsplash.com/photo-1594675610313-f427344ac988?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxhbWF6b24lMjByaXZlcnxlbnwwfHx8fDE3NTc0NDE3Njh8MA&ixlib=rb-4.1.0&q=85",
        "instagram": "@restodavila",
        "hasPool": True,
        "hours": "Almoço - das 11h às 15h",
        "phones": ["(91) 98822-3201"],
        "categories": ["restaurants", "piscina", "igarape-combu"],
        "location": "9.2 km - Icoaraci",
        "comments": "17 avaliações",
        "rating": 4.4,
        "cuisine": "Brasileira, Frutos do mar"
    },
    {
        "name": "White House Icoaraci",
        "image": "https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg",
        "instagram": "@whitehouseicoaraci",
        "hasPool": False,
        "hours": "Fechado hoje - Consulte horários",
        "phones": ["(91) 99240-7845"],
        "categories": ["restaurants"],
        "location": "9.1 km - Icoaraci",
        "comments": "1 avaliação",
        "rating": 5.0,
        "cuisine": "Brasileira, Pub"
    },
    {
        "name": "Restaurante Maia",
        "image": "https://images.pexels.com/photos/33664253/pexels-photo-33664253.jpeg",
        "instagram": "@restaurantemaiabelem",
        "hasPool": False,
        "hours": "Almoço e jantar - das 11h às 22h",
        "phones": ["(91) 99161-8019", "(91) 99273-9149"],
        "categories": ["restaurants", "furo-paciencia"],
        "location": "9.2 km - Furo da Paciência",
        "comments": "16 avaliações",
        "rating": 4.3,
        "cuisine": "Brasileira, Sul-americana"
    },
    {
        "name": "O Boteco",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxyZXN0YXVyYW50fGVufDB8fHx8MTc1NzQ0MTgwMnww&ixlib=rb-4.1.0&q=85",
        "instagram": "@obotecoicoaraci",
        "hasPool": False,
        "hours": "Happy hour - das 17h às 23h",
        "phones": ["(91) 98229-0151"],
        "categories": ["restaurants"],
        "location": "9.2 km - Icoaraci",
        "comments": "5 avaliações",
        "rating": 4.6,
        "cuisine": "Bar, Petiscos"
    },
    {
        "name": "Restaurante do Anibal",
        "image": "https://images.unsplash.com/photo-1620898670223-6f7f07d82a3b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxlY28lMjB0b3VyaXNtfGVufDB8fHx8MTc1NzQ0MTgxMHww&ixlib=rb-4.1.0&q=85",
        "instagram": "@anibalbelem",
        "hasPool": False,
        "hours": "Almoço - das 11h às 15h",
        "phones": ["(91) 99371-4119"],
        "categories": ["restaurants", "furo-sao-benedito"],
        "location": "9.2 km - Furo do São Benedito",
        "comments": "2 avaliações",
        "rating": 4.0,
        "cuisine": "Brasileira, Familiar"
    },
    {
        "name": "Ponto Do Chef",
        "image": "https://images.unsplash.com/photo-1591081658714-f576fb7ea3ed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxhbWF6b24lMjByaXZlcnxlbnwwfHx8fDE3NTc0NDE3Njh8MA&ixlib=rb-4.1.0&q=85",
        "instagram": "@pontodochef",
        "hasPool": False,
        "hours": "Aberto agora - das 11h às 22h",
        "phones": ["(91) 98733-6518"],
        "categories": ["restaurants"],
        "location": "9.2 km - Icoaraci",
        "comments": "7 avaliações",
        "rating": 3.4,
        "cuisine": "Brasileira, Executiva"
    },
    {
        "name": "Pizzaria Porao Italia",
        "image": "https://images.unsplash.com/photo-1594675610313-f427344ac988?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxhbWF6b24lMjByaXZlcnxlbnwwfHx8fDE3NTc0NDE3Njh8MA&ixlib=rb-4.1.0&q=85",
        "instagram": "@poraoitalia",
        "hasPool": False,
        "hours": "Jantar - das 18h às 23h",
        "phones": ["(91) 99240-7945"],
        "categories": ["restaurants"],
        "location": "9.2 km - Icoaraci",
        "comments": "9 avaliações",
        "rating": 3.6,
        "cuisine": "Italiana, Pizza"
    },
    {
        "name": "Boi Novo Churrascaria",
        "image": "https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg",
        "instagram": "@boinovochurrascaria",
        "hasPool": False,
        "hours": "Almoço e jantar - das 11h às 22h",
        "phones": ["(91) 99388-8885", "(91) 9188-0108"],
        "categories": ["restaurants"],
        "location": "13.7 km - Região Metropolitana",
        "comments": "101 avaliações",
        "rating": 4.1,
        "cuisine": "Brasileira, Churrasco"
    },
    {
        "name": "Tokyo Temakeria",
        "image": "https://images.pexels.com/photos/33664253/pexels-photo-33664253.jpeg",
        "instagram": "@tokyotemakeriabelem",
        "hasPool": False,
        "hours": "Fechado agora - das 18h às 23h",
        "phones": ["(91) 99903-3314"],
        "categories": ["restaurants"],
        "location": "13.7 km - Região Metropolitana",
        "comments": "66 avaliações",
        "rating": 4.0,
        "cuisine": "Japonesa, Sushi"
    },
    {
        "name": "Bigas Lanche",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxyZXN0YXVyYW50fGVufDB8fHx8MTc1NzQ0MTgwMnww&ixlib=rb-4.1.0&q=85",
        "instagram": "@bigaslanche",
        "hasPool": False,
        "hours": "Das 18h às 02h - Lanches noturnos",
        "phones": ["(91) 98229-0150"],
        "categories": ["restaurants"],
        "location": "13.5 km",
        "comments": "5 avaliações",
        "rating": 3.6,
        "cuisine": "Lanches, Fast Food"
    },
    {
        "name": "Helenas Bar",
        "image": "https://images.unsplash.com/photo-1620898670223-6f7f07d82a3b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxlY28lMjB0b3VyaXNtfGVufDB8fHx8MTc1NzQ0MTgxMHww&ixlib=rb-4.1.0&q=85",
        "instagram": "@helenasbar",
        "hasPool": False,
        "hours": "Happy hour - das 17h às 01h",
        "phones": ["(91) 98822-3200"],
        "categories": ["restaurants"],
        "location": "13.7 km",
        "comments": "2 avaliações",
        "rating": 3.0,
        "cuisine": "Bares e pubs, Bar"
    },
    {
        "name": "Secundino Lanches",
        "image": "https://images.unsplash.com/photo-1591081658714-f576fb7ea3ed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxhbWF6b24lMjByaXZlcnxlbnwwfHx8fDE3NTc0NDE3Njh8MA&ixlib=rb-4.1.0&q=85",
        "instagram": "@secundinolanches",
        "hasPool": False,
        "hours": "Das 18h às 02h",
        "phones": ["(91) 9964-2701"],
        "categories": ["restaurants"],
        "location": "14.7 km",
        "comments": "2 avaliações", 
        "rating": 5.0,
        "cuisine": "Lanches, Comida caseira"
    }
]

async def seed_restaurants():
    """Popula o banco de dados com dados iniciais dos restaurantes"""
    
    print("🌱 Iniciando seed do banco de dados...")
    
    # Verificar se já existem restaurantes
    existing_count = await db.restaurants.count_documents({})
    
    if existing_count > 0:
        print(f"ℹ️ Banco já possui {existing_count} restaurantes")
        response = input("Deseja limpar e recriar os dados? (y/n): ")
        if response.lower() == 'y':
            await db.restaurants.delete_many({})
            print("🗑️ Dados anteriores removidos")
        else:
            print("❌ Operação cancelada")
            return
    
    # Inserir restaurantes
    restaurants_to_insert = []
    
    for restaurant_data in RESTAURANT_DATA:
        restaurant = Restaurant(**restaurant_data)
        restaurants_to_insert.append(restaurant.dict())
    
    # Inserir em lote
    result = await db.restaurants.insert_many(restaurants_to_insert)
    
    print(f"✅ {len(result.inserted_ids)} restaurantes inseridos com sucesso!")
    
    # Criar índices para melhor performance
    await db.restaurants.create_index("name")
    await db.restaurants.create_index("categories")
    await db.restaurants.create_index("rating")
    await db.restaurants.create_index("hasPool")
    await db.restaurants.create_index([("name", "text"), ("location", "text"), ("cuisine", "text")])
    
    print("📊 Índices criados para otimização de busca")
    
    # Estatísticas
    total = await db.restaurants.count_documents({})
    with_pool = await db.restaurants.count_documents({"hasPool": True})
    avg_rating = await db.restaurants.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}
    ]).to_list(1)
    
    print(f"📈 Estatísticas finais:")
    print(f"   - Total de restaurantes: {total}")
    print(f"   - Restaurantes com piscina: {with_pool}")
    print(f"   - Avaliação média: {round(avg_rating[0]['avg'], 2) if avg_rating else 'N/A'}")
    
    # Fechar conexão
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_restaurants())