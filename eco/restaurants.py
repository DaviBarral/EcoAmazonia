from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models.restaurant import Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantSearch, Category
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import re

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# MongoDB connection
from server import db

# Categories data
CATEGORIES = [
    {"id": "all", "name": "Todos"},
    {"id": "restaurants", "name": "Restaurantes"},
    {"id": "piscina", "name": "Piscina"},
    {"id": "rio-guama", "name": "Rio Guamá"},
    {"id": "igarape-combu", "name": "Igarapé do Combu"},
    {"id": "hospedagem", "name": "Com Hospedagem"},
    {"id": "furo-paciencia", "name": "Furo da Paciência"},
    {"id": "furo-sao-benedito", "name": "Furo do São Benedito"},
    {"id": "piriquitaquara", "name": "Ig. do Piriquitaquara"}
]

@router.get("/categories", response_model=List[Category])
async def get_categories():
    """Retorna todas as categorias disponíveis"""
    return CATEGORIES

@router.get("/", response_model=List[Restaurant])
async def get_restaurants(
    search: Optional[str] = Query(None, description="Buscar por nome do restaurante"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    hasPool: Optional[bool] = Query(None, description="Filtrar por piscina"),
    rating_min: Optional[float] = Query(None, ge=0, le=5, description="Avaliação mínima"),
    rating_max: Optional[float] = Query(None, ge=0, le=5, description="Avaliação máxima"),
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    skip: int = Query(0, ge=0, description="Pular resultados")
):
    """Retorna lista de restaurantes com filtros opcionais"""
    
    # Construir filtros
    filters = {}
    
    if search:
        filters["name"] = {"$regex": search, "$options": "i"}
    
    if category and category != "all":
        filters["categories"] = {"$in": [category]}
    
    if hasPool is not None:
        filters["hasPool"] = hasPool
    
    if rating_min is not None or rating_max is not None:
        rating_filter = {}
        if rating_min is not None:
            rating_filter["$gte"] = rating_min
        if rating_max is not None:
            rating_filter["$lte"] = rating_max
        filters["rating"] = rating_filter
    
    # Buscar no banco
    cursor = db.restaurants.find(filters).skip(skip).limit(limit).sort("name", 1)
    restaurants = await cursor.to_list(length=limit)
    
    return [Restaurant(**restaurant) for restaurant in restaurants]

@router.get("/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(restaurant_id: str):
    """Retorna um restaurante específico"""
    restaurant = await db.restaurants.find_one({"id": restaurant_id})
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    return Restaurant(**restaurant)

@router.post("/", response_model=Restaurant)
async def create_restaurant(restaurant: RestaurantCreate):
    """Cria um novo restaurante"""
    
    # Verificar se já existe um restaurante com o mesmo nome
    existing = await db.restaurants.find_one({"name": {"$regex": f"^{re.escape(restaurant.name)}$", "$options": "i"}})
    if existing:
        raise HTTPException(status_code=400, detail="Já existe um restaurante com este nome")
    
    # Criar novo restaurante
    new_restaurant = Restaurant(**restaurant.dict())
    
    # Inserir no banco
    await db.restaurants.insert_one(new_restaurant.dict())
    
    return new_restaurant

@router.put("/{restaurant_id}", response_model=Restaurant)
async def update_restaurant(restaurant_id: str, restaurant_update: RestaurantUpdate):
    """Atualiza um restaurante existente"""
    
    # Verificar se o restaurante existe
    existing = await db.restaurants.find_one({"id": restaurant_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    # Preparar dados para atualização
    update_data = {k: v for k, v in restaurant_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    # Verificar se o nome não está sendo usado por outro restaurante
    if "name" in update_data:
        name_check = await db.restaurants.find_one({
            "name": {"$regex": f"^{re.escape(update_data['name'])}$", "$options": "i"},
            "id": {"$ne": restaurant_id}
        })
        if name_check:
            raise HTTPException(status_code=400, detail="Já existe outro restaurante com este nome")
    
    # Atualizar no banco
    await db.restaurants.update_one(
        {"id": restaurant_id},
        {"$set": update_data}
    )
    
    # Retornar restaurante atualizado
    updated_restaurant = await db.restaurants.find_one({"id": restaurant_id})
    return Restaurant(**updated_restaurant)

@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    """Remove um restaurante"""
    
    # Verificar se o restaurante existe
    existing = await db.restaurants.find_one({"id": restaurant_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    # Remover do banco
    await db.restaurants.delete_one({"id": restaurant_id})
    
    return {"message": "Restaurante removido com sucesso"}

@router.get("/search/suggestions")
async def get_search_suggestions(q: str = Query(..., min_length=1, description="Termo de busca")):
    """Retorna sugestões de busca baseadas no nome dos restaurantes"""
    
    suggestions = await db.restaurants.find(
        {"name": {"$regex": q, "$options": "i"}},
        {"name": 1, "_id": 0}
    ).limit(5).to_list(5)
    
    return [suggestion["name"] for suggestion in suggestions]

@router.get("/stats/overview")
async def get_restaurant_stats():
    """Retorna estatísticas gerais dos restaurantes"""
    
    total_restaurants = await db.restaurants.count_documents({})
    
    restaurants_with_pool = await db.restaurants.count_documents({"hasPool": True})
    
    # Estatísticas por categoria
    pipeline = [
        {"$unwind": "$categories"},
        {"$group": {"_id": "$categories", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    category_stats = await db.restaurants.aggregate(pipeline).to_list(None)
    
    # Média de avaliações
    rating_pipeline = [
        {"$match": {"rating": {"$ne": None}}},
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}, "count": {"$sum": 1}}}
    ]
    rating_stats = await db.restaurants.aggregate(rating_pipeline).to_list(1)
    
    return {
        "total_restaurants": total_restaurants,
        "restaurants_with_pool": restaurants_with_pool,
        "pool_percentage": round((restaurants_with_pool / total_restaurants * 100), 2) if total_restaurants > 0 else 0,
        "category_distribution": category_stats,
        "average_rating": round(rating_stats[0]["avg_rating"], 2) if rating_stats else 0,
        "rated_restaurants": rating_stats[0]["count"] if rating_stats else 0
    }