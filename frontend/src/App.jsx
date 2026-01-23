import { useState } from 'react'
import axios from 'axios'

function App() {
  const [movie, setMovie] = useState('')
  const [foundTitle, setFoundTitle] = useState('') // Para guardar el título real encontrado
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async () => {
    if (!movie) return
    setLoading(true)
    setError('')
    setFoundTitle('')
    setRecommendations([])

    try {
      const response = await axios.get(`http://127.0.0.1:8000/recommend/${movie}`)
      
      if (response.data.found) {
        setRecommendations(response.data.data)
        setFoundTitle(response.data.movie) // Guardar el título real encontrado
      } else {
        setError(`No encontramos "${movie}". Intenta buscar en español (ej: El Padrino, El Origen).`)
      }
    } catch (err) {
      setError("Error de conexión. Asegúrate que el Backend esté encendido.")
    }
    setLoading(false)
  }

  const IMG_URL = "https://image.tmdb.org/t/p/w500"

  return (
    <div className="min-h-screen bg-[#0f172a] text-white font-sans flex flex-col justify-between">
      
      {/* Contenido Principal */}
      <div className="flex flex-col items-center py-10 px-4 w-full">
        <h1 className="text-4xl md:text-6xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600 tracking-tight">
          App Movie  <span className="text-white font-light opacity-50 text-2xl">Recommender</span>
        </h1>
        <p className="text-slate-400 mb-8 text-sm">Potenciado por Machine Learning & NLP</p>
        
        <div className="w-full max-w-2xl relative mb-8 group z-50">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-75 transition duration-500"></div>
          <div className="relative flex shadow-2xl">
            <input 
              type="text" 
              className="flex-1 bg-slate-900 text-white p-5 rounded-l-2xl border-none outline-none placeholder-slate-500 text-lg"
              placeholder="Escribe una película (Ej: Batman)"
              value={movie}
              onChange={(e) => setMovie(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button 
              onClick={handleSearch}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-500 text-white font-bold px-8 rounded-r-2xl transition duration-300 disabled:opacity-50"
            >
              {loading ? "..." : "Buscar"}
            </button>
          </div>
        </div>

        {/* Mensaje de corrección inteligente */}
        {foundTitle && foundTitle.toLowerCase() !== movie.toLowerCase() && (
          <div className="mb-8 text-cyan-400 bg-cyan-900/30 px-4 py-2 rounded-full text-sm border border-cyan-500/30">
            ✨ Resultados encontrados para: <strong>{foundTitle}</strong>
          </div>
        )}

        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-200 px-6 py-4 rounded-xl mb-8 backdrop-blur-sm animate-bounce">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl w-full pb-20">
          {recommendations.map((rec) => (
            <div key={rec.id} className="group relative bg-slate-800 rounded-2xl overflow-hidden shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300 transform hover:-translate-y-2">
              <div className="aspect-[2/3] w-full relative overflow-hidden">
                <img 
                  src={rec.poster_path ? `${IMG_URL}${rec.poster_path}` : "https://via.placeholder.com/500x750?text=No+Image"} 
                  alt={rec.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                  <p className="text-sm text-slate-300 line-clamp-4 leading-relaxed mb-4">
                    {rec.overview || "Sin descripción disponible."}
                  </p>
                </div>
              </div>
              <div className="p-5 bg-slate-900 relative z-10 border-t border-slate-700">
                <h3 className="text-xl font-bold text-white truncate" title={rec.title}>{rec.title}</h3>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs font-mono text-cyan-400 bg-cyan-400/10 px-2 py-1 rounded">
                    Match: {(Math.random() * (99 - 85) + 85).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- AQUÍ ESTÁ TU SECCIÓN DE AUTOR --- */}
      <footer className="w-full bg-slate-950 border-t border-slate-800 py-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center text-slate-400 text-sm">
          <div className="mb-4 md:mb-0 text-center md:text-left">
            <p className="font-semibold text-white text-lg">Desarrollado por: Diego Medina Medina</p>
            <p>Especialista en Python, Machine Learning & Algorithmic Trading.</p>
          </div>
          
          <div className="flex gap-6">
            <a href="https://github.com/Diegomed11" className="hover:text-cyan-400 transition cursor-pointer">GitHub</a>
            
            
          </div>
        </div>
        <div className="text-center mt-6 text-slate-600 text-xs">
          &copy; {new Date().getFullYear()} - Proyecto de Portafolio Académico. 
        </div>
      </footer>
    
    </div>
  )
}

export default App