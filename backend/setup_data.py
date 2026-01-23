import pandas as pd
import requests
import time
import os


API_KEY = '' 
OUTPUT_FILE = "app/data/movies.csv"
LANGUAGE = 'es-MX'

def get_movies(pages=25): # Aumentamos a 25 páginas (500 pelis)
    print(f"📡 Descargando catálogo de películas populares ({pages*20} títulos)...")
    movies = []
    # CAMBIO: Usamos 'popular' en vez de 'top_rated' para tener éxitos modernos
    url = "https://api.themoviedb.org/3/movie/popular"
    
    for page in range(1, pages + 1):
        try:
            res = requests.get(url, params={'api_key': API_KEY, 'language': LANGUAGE, 'page': page})
            res.raise_for_status()
            data = res.json()
            movies.extend(data.get('results', []))
            print(f"   ✅ Página {page}/{pages} lista.")
        except Exception as e:
            print(f"   ❌ Error en página {page}: {e}")
            break
    return movies

def get_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {'api_key': API_KEY, 'language': LANGUAGE, 'append_to_response': 'keywords,credits'}
    try:
        res = requests.get(url, params=params)
        return res.json() if res.status_code == 200 else None
    except:
        return None

def process_features(details):
    if not details: return ""
    genres = [d['name'] for d in details.get('genres', [])]
    keywords = [d['name'] for d in details.get('keywords', {}).get('keywords', [])]
    cast = [d['name'] for d in details.get('credits', {}).get('cast', [])[:4]] # Top 4 actores
    
    director = ""
    for crew in details.get('credits', {}).get('crew', []):
        if crew['job'] == 'Director':
            director = crew['name']
            break
            
    # Creamos la "sopa de letras" para la IA
    features = genres + keywords + cast + [director]
    clean_features = [str(x).replace(" ", "").lower() for x in features if x]
    return " ".join(clean_features)

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    raw_movies = get_movies(pages=25) 
    clean_data = []
    total = len(raw_movies)
    
    print(f"\n⚙️ Procesando detalles (esto tomará unos minutos, ten paciencia)...")
    
    for i, movie in enumerate(raw_movies):
        m_id = movie['id']
        # CAMBIO CLAVE: Guardamos ambos títulos
        title_es = movie['title']
        title_en = movie.get('original_title', '') 
        
        details = get_details(m_id)
        features = process_features(details)
        
        clean_data.append({
            'id': m_id,
            'title': title_es,           # Título en Español (El Origen)
            'original_title': title_en,  # Título en Inglés (Inception)
            'features': features,
            'overview': movie.get('overview', ''),
            'poster_path': movie.get('poster_path', '')
        })
        
        if i % 10 == 0:
            print(f"   Procesando... {i}/{total}")
        
        time.sleep(0.02) 

    df = pd.DataFrame(clean_data)
    # Eliminamos duplicados por si acaso
    df = df.drop_duplicates(subset=['id'])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n🎉 ¡ÉXITO! Base de datos actualizada con {len(df)} películas.")

if __name__ == "__main__":
    main()