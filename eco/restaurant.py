from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import uuid

class Category(BaseModel):
    id: str
    name: str

class Restaurant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=200)
    image: str = Field(..., description="URL da imagem do restaurante")
    instagram: Optional[str] = Field(None, description="Handle do Instagram")
    hasPool: bool = Field(default=False, description="Se tem piscina")
    hours: str = Field(..., description="Horário de funcionamento")
    phones: List[str] = Field(..., description="Lista de telefones")
    email: Optional[str] = Field(None, description="Email de contato")
    categories: List[str] = Field(..., description="Lista de IDs de categorias")
    location: str = Field(..., description="Localização do restaurante")
    comments: str = Field(default="Nenhum comentário")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Avaliação de 0 a 5")
    cuisine: Optional[str] = Field(None, description="Tipo de culinária")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('phones')
    def validate_phones(cls, v):
        if not v:
            raise ValueError('Pelo menos um telefone deve ser fornecido')
        return v
    
    @validator('categories')
    def validate_categories(cls, v):
        if not v:
            raise ValueError('Pelo menos uma categoria deve ser fornecida')
        return v

class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    image: str
    instagram: Optional[str] = None
    hasPool: bool = False
    hours: str
    phones: List[str]
    email: Optional[str] = None
    categories: List[str]
    location: str
    comments: str = "Nenhum comentário"
    rating: Optional[float] = Field(None, ge=0, le=5)
    cuisine: Optional[str] = None

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    image: Optional[str] = None
    instagram: Optional[str] = None
    hasPool: Optional[bool] = None
    hours: Optional[str] = None
    phones: Optional[List[str]] = None
    email: Optional[str] = None
    categories: Optional[List[str]] = None
    location: Optional[str] = None
    comments: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    cuisine: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RestaurantSearch(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    hasPool: Optional[bool] = None
    rating_min: Optional[float] = Field(None, ge=0, le=5)
    rating_max: Optional[float] = Field(None, ge=0, le=5)