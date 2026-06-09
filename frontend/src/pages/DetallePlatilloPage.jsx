import { useState, useEffect } from 'react';
import { obtenerPlatillo } from '../services/api';
import './DetallePlatilloPage.css';

function DetallePlatilloPage({ platilloId, onVolver, onPreguntarChef, onVerIngredientes }) {
  const [platillo, setPlatillo] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      try {
        const data = await obtenerPlatillo(platilloId);
        setPlatillo(data);
      } catch (error) {
        console.error('Error cargando platillo:', error);
      } finally {
        setCargando(false);
      }
    };
    cargar();
  }, [platilloId]);

  if (cargando) return <div className="detalle-page"><div className="detalle-cargando">Cargando receta...</div></div>;
  if (!platillo) return <div className="detalle-page"><div className="detalle-cargando">Platillo no encontrado</div></div>;

  return (
    <div className="detalle-page">
      <header className="detalle-header">
        <button className="btn-volver-detalle" onClick={onVolver}>← Catálogo</button>
      </header>

      <div className="detalle-contenido">
        <div className="detalle-imagen">
          <img src={`/images/platillos/${platillo.imagen}`} alt={platillo.nombre} />
          <span className="detalle-nivel">{platillo.nivel}</span>
        </div>

        <div className="detalle-info-principal">
          <h1>{platillo.nombre}</h1>
          <p className="detalle-cocina">{platillo.cocina} · {platillo.pais}</p>

          <div className="detalle-meta">
            {platillo.tiempo_preparacion && <span>⏱️ {platillo.tiempo_preparacion}</span>}
            {platillo.porciones && <span>🍽️ {platillo.porciones} porciones</span>}
            <span>🌍 {platillo.continente}</span>
          </div>
        </div>

        {platillo.descripcion && (
          <div className="detalle-seccion">
            <h2>Descripción</h2>
            <p>{platillo.descripcion}</p>
          </div>
        )}

        {platillo.historia && (
          <div className="detalle-seccion">
            <h2>📜 Historia</h2>
            <p>{platillo.historia}</p>
          </div>
        )}

        {platillo.tip_chef && (
          <div className="detalle-seccion detalle-tip">
            <h2>👨‍🍳 Tip del Chef Vittorio</h2>
            <p>{platillo.tip_chef}</p>
          </div>
        )}

        {platillo.ingredientes && platillo.ingredientes.length > 0 && (
          <div className="detalle-seccion">
            <h2>🥘 Ingredientes</h2>
            <div className="detalle-ingredientes">
              {platillo.ingredientes.map((ing, i) => (
                <div key={i} className="detalle-ingrediente">
                  <span className="ing-cantidad">{ing.cantidad}</span>
                  <span className="ing-nombre">{ing.nombre}</span>
                  {ing.notas && <span className="ing-notas">({ing.notas})</span>}
                </div>
              ))}
            </div>
          </div>
        )}

        {platillo.pasos && platillo.pasos.length > 0 && (
          <div className="detalle-seccion">
            <h2>📋 Pasos</h2>
            <div className="detalle-pasos">
              {platillo.pasos.map((paso, i) => (
                <div key={i} className="detalle-paso">
                  <div className="paso-numero">{paso.num_paso}</div>
                  <div className="paso-contenido">
                    <p>{paso.instruccion}</p>
                    {paso.tip_chef && <p className="paso-tip">💡 {paso.tip_chef}</p>}
                    {paso.tiempo_minutos && <span className="paso-tiempo">⏱️ {paso.tiempo_minutos} min</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="detalle-acciones">
            
          <button className="btn-chef" onClick={() => onPreguntarChef(`Enséñame a hacer ${platillo.nombre} paso a paso`)}>
            👨‍🍳 Pregúntale al Chef
          </button>
          <button className="btn-ingredientes" onClick={() => onVerIngredientes(platilloId, platillo.nombre)}>
            📝 Lista de Ingredientes
          </button>
        </div>
      </div>
    </div>
  );
}

export default DetallePlatilloPage;
