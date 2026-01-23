from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import MovieRecommender
import os

app = FastAPI(title="CineAI API")

# Permitir que React (Frontend) hable con FastAPI (Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción esto se cambia por el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable global para el recomendador
recommender = None

@app.on_event("startup")
def startup_event():
    global recommender
    # Intentamos iniciar el recomendador
    try:
        recommender = MovieRecommender()
        print("✅ Modelo de IA cargado correctamente.")
    except Exception as e:
        print(f"⚠️ Error cargando modelo: {e}")
        print("El servidor funcionará, pero las recomendaciones fallarán hasta que generes el 'movies.csv'")

@app.get("/")
def read_root():
    return {"status": "Online", "service": "CineAI Recommender"}

@app.get("/recommend/{movie_title}")
def recommend(movie_title: str):
    if not recommender:
        raise HTTPException(status_code=503, detail="Model not loaded")
        
    # Llamamos a la nueva lógica
    response = recommender.get_recommendations(movie_title)
    
    # Si devuelve lista vacía es que no encontró nada
    if not response:
        return {"found": False, "message": "Película no encontrada", "data": []}
        
    return {
        "found": True, 
        "movie": response["original_title"], # Devolvemos el nombre real que encontró (ej: "El Origen")
        "data": response["results"]
    }