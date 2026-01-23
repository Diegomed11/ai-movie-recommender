import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import os

class MovieRecommender:
    def __init__(self, data_path="app/data/movies.csv"):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No encontré {data_path}. Ejecuta python setup_data.py primero.")
            
        self.df = pd.read_csv(data_path)
        self.df['features'] = self.df['features'].fillna('')
        
        # Entrenar IA
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        # Índices para búsqueda rápida (en minúsculas para facilitar)
        self.df['title_lower'] = self.df['title'].str.lower()
        self.df['original_lower'] = self.df['original_title'].str.lower()

    def get_recommendations(self, query):
        query = query.lower().strip()
        
        # 1. Búsqueda EXACTA (en español O inglés)
        match = self.df[
            (self.df['title_lower'] == query) | 
            (self.df['original_lower'] == query)
        ]
        
        idx = None
        found_title = ""
        
        if not match.empty:
            idx = match.index[0]
            found_title = match.iloc[0]['title']
        else:
            # 2. Búsqueda DIFUSA (Aproximada)
            # Buscamos en ambas columnas y juntamos las opciones
            all_titles = self.df['title_lower'].tolist() + self.df['original_lower'].tolist()
            matches = difflib.get_close_matches(query, all_titles, n=1, cutoff=0.5)
            
            if not matches:
                return []
            
            best_match = matches[0]
            # Encontrar a qué película pertenece ese match
            match_row = self.df[
                (self.df['title_lower'] == best_match) | 
                (self.df['original_lower'] == best_match)
            ]
            
            if not match_row.empty:
                idx = match_row.index[0]
                found_title = match_row.iloc[0]['title']
        
        if idx is None:
            return []

        # Calcular similitudes
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:7]
        
        movie_indices = [i[0] for i in sim_scores]
        
        results = self.df.iloc[movie_indices][['title', 'id', 'poster_path', 'overview']].to_dict(orient='records')
        
        return {"original_title": found_title, "results": results}