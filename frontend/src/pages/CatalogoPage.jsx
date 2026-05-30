import { useState, useEffect } from 'react';
import { listarPlatillos, obtenerIdsFavoritos, agregarFavorito, quitarFavorito } from '../services/api';
import './CatalogoPage.css';

const continentes = ['Todos', 'Europa', 'Asia', 'América', 'África', 'Oceanía', '❤️ Favoritos'];

function CatalogoPage({ onVolverAlChat, onPreguntarPlatillo, onVerListaCompras }) {
  const [platillos, setPlatillos] = useState([]);
  const [favoritosIds, setFavoritosIds] = useState([]);
  const [filtroContinente, setFiltroContinente] = useState('Todos');
  const [filtroPais, setFiltroPais] = useState(null);
  const [busqueda, setBusqueda] = useState('');
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      try {
        const [data, favs] = await Promise.all([
          listarPlatillos(),
          obtenerIdsFavoritos()
        ]);
        setPlatillos(data);
        setFavoritosIds(favs);
      } catch (error) {
        console.error('Error cargando platillos:', error);
      } finally {
        setCargando(false);
      }
    };
    cargar();
  }, []);

  const toggleFavorito = async (platilloId) => {
    try {
      if (favoritosIds.includes(platilloId)) {
        await quitarFavorito(platilloId);
        setFavoritosIds((prev) => prev.filter((id) => id !== platilloId));
      } else {
        await agregarFavorito(platilloId);
        setFavoritosIds((prev) => [...prev, platilloId]);
      }
    } catch (error) {
      console.error('Error toggling favorito:', error);
    }
  };

  const handleContinente = (continente) => {
    setFiltroContinente(continente);
    setFiltroPais(null);
  };

  const paisesDelContinente = filtroContinente !== 'Todos' && filtroContinente !== '❤️ Favoritos'
    ? [...new Set(platillos.filter(p => p.continente === filtroContinente).map(p => p.pais))]
    : [];

  const platillosPorFiltro = filtroContinente === 'Todos'
    ? platillos
    : filtroContinente === '❤️ Favoritos'
    ? platillos.filter((p) => favoritosIds.includes(p.id))
    : filtroPais
    ? platillos.filter((p) => p.pais === filtroPais)
    : platillos.filter((p) => p.continente === filtroContinente);

  const platillosFiltrados = busqueda
    ? platillosPorFiltro.filter((p) => p.nombre.toLowerCase().includes(busqueda.toLowerCase()))
    : platillosPorFiltro;

  return (
    <div className="catalogo-page">
      <header className="catalogo-header">
        <button className="btn-volver" onClick={onVolverAlChat}>
          ← Chef Vittorio
        </button>
        <div className="catalogo-titulo">
          <h1>Catálogo Mundial</h1>
          <p>{platillos.length} platillos de 5 continentes</p>
        </div>
      </header>

      <div className="buscador">
        <input
          type="text"
          className="buscador-input"
          placeholder="Buscar platillo..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        {busqueda && (
          <button className="buscador-clear" onClick={() => setBusqueda('')}>✕</button>
        )}
      </div>

      <div className="filtros">
        {continentes.map((c) => (
          <button
            key={c}
            className={`filtro-btn ${filtroContinente === c ? 'activo' : ''}`}
            onClick={() => handleContinente(c)}
          >
            {c}
          </button>
        ))}
      </div>

      {paisesDelContinente.length > 0 && (
        <div className="filtros filtros-paises">
          <button
            className={`filtro-pais-btn ${filtroPais === null ? 'activo' : ''}`}
            onClick={() => setFiltroPais(null)}
          >
            Todos los países
          </button>
          {paisesDelContinente.map((pais) => (
            <button
              key={pais}
              className={`filtro-pais-btn ${filtroPais === pais ? 'activo' : ''}`}
              onClick={() => setFiltroPais(pais)}
            >
              {pais}
            </button>
          ))}
        </div>
      )}

      {cargando ? (
        <div className="cargando">Cargando platillos...</div>
      ) : (
        <div className="platillos-grid">
          {platillosFiltrados.length === 0 ? (
            <div className="sin-resultados">
              {busqueda
                ? `No se encontraron platillos con "${busqueda}"`
                : filtroContinente === '❤️ Favoritos'
                ? 'Aún no tienes favoritos. Dale ❤️ a los platillos que te gusten.'
                : 'No se encontraron platillos.'}
            </div>
          ) : (
            platillosFiltrados.map((p) => (
              <div key={p.id} className="platillo-card">
                <div className="platillo-img-container">
                  <img
                    src={`/images/platillos/${p.imagen}`}
                    alt={p.nombre}
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                  <span className="platillo-nivel">{p.nivel}</span>
                  <button
                    className={`btn-favorito ${favoritosIds.includes(p.id) ? 'es-favorito' : ''}`}
                    onClick={() => toggleFavorito(p.id)}
                  >
                    {favoritosIds.includes(p.id) ? '❤️' : '🤍'}
                  </button>
                  <div className="platillo-overlay">
                    <p>{p.descripcion}</p>
                  </div>
                </div>
                <div className="platillo-info">
                  <h3>{p.nombre}</h3>
                  <p className="platillo-cocina">{p.cocina}</p>
                  <div className="platillo-meta">
                    <span className="platillo-pais">{p.pais}</span>
                    <span className="platillo-continente">{p.continente}</span>
                  </div>
                  <div className="platillo-botones">
                    <button
                      className="btn-cocinar"
                      onClick={() => onPreguntarPlatillo(`Enséñame a hacer ${p.nombre} paso a paso`)}
                    >
                      👨‍🍳 Cocinar
                    </button>
                    <button
                      className="btn-lista"
                      onClick={() => onVerListaCompras(p.id, p.nombre)}
                    >
                      📝 Ingredientes
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default CatalogoPage;
