import { useState, useEffect } from 'react';
import { obtenerPerfil } from '../services/api';
import './PerfilPage.css';

function PerfilPage({ usuario, onVolver }) {
  const [perfil, setPerfil] = useState(null);
  const [logros, setLogros] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      try {
        const perfilData = await obtenerPerfil();
        setPerfil(perfilData);
        const response = await fetch('http://localhost:8000/perfil/logros', {
          headers: { 'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem('chef_usuario')).token }
        });
        const logrosData = await response.json();
        setLogros(logrosData);
      } catch (e) {
        console.error('Error cargando perfil:', e);
      } finally {
        setCargando(false);
      }
    };
    cargar();
  }, []);

  if (cargando) return <div className="perfil-page"><div className="perfil-cargando">Cargando tu perfil...</div></div>;
  if (!perfil) return <div className="perfil-page"><div className="perfil-cargando">Error cargando perfil</div></div>;

  const xpProgreso = perfil.xp_siguiente
    ? ((perfil.xp - perfil.xp_minimo) / (perfil.xp_siguiente - perfil.xp_minimo)) * 100
    : 100;

  const logrosDesbloqueados = logros.filter(l => l.desbloqueado).length;

  return (
    <div className="perfil-page">
      <header className="perfil-header">
        <button className="btn-volver-perfil" onClick={onVolver}>← Volver</button>
        <h1>Mi Perfil</h1>
      </header>

      <div className="perfil-contenido">
        <div className="perfil-usuario">
          <div className="perfil-avatar">
            <span>{perfil.nivel_icono}</span>
          </div>
          <h2>{usuario.nombre}</h2>
          <p className="perfil-email">{usuario.email}</p>
          <span className="perfil-nivel-badge">{perfil.nivel_icono} {perfil.nivel}</span>
        </div>

        <div className="perfil-xp-card">
          <div className="xp-header">
            <span className="xp-label">Experiencia</span>
            <span className="xp-valor">{perfil.xp} XP</span>
          </div>
          <div className="xp-barra">
            <div className="xp-barra-fill" style={{ width: `${Math.min(xpProgreso, 100)}%` }}></div>
          </div>
          <div className="xp-footer">
            <span>{perfil.xp_minimo} XP</span>
            <span>{perfil.xp_siguiente ? `${perfil.xp_siguiente} XP` : 'Nivel máximo'}</span>
          </div>
        </div>

        <div className="perfil-stats">
          <div className="stat-card">
            <span className="stat-icono">🔥</span>
            <span className="stat-valor">{perfil.racha}</span>
            <span className="stat-label">Racha actual</span>
          </div>
          <div className="stat-card">
            <span className="stat-icono">⭐</span>
            <span className="stat-valor">{perfil.mejor_racha}</span>
            <span className="stat-label">Mejor racha</span>
          </div>
          <div className="stat-card">
            <span className="stat-icono">💬</span>
            <span className="stat-valor">{perfil.preguntas_al_chef}</span>
            <span className="stat-label">Preguntas</span>
          </div>
          <div className="stat-card">
            <span className="stat-icono">🏆</span>
            <span className="stat-valor">{logrosDesbloqueados}/{perfil.logros_totales}</span>
            <span className="stat-label">Logros</span>
          </div>
        </div>

        <div className="perfil-logros">
          <h3>Logros</h3>
          <div className="logros-grid">
            {logros.map((logro) => (
              <div key={logro.id} className={`logro-card ${logro.desbloqueado ? 'desbloqueado' : 'bloqueado'}`}>
                <span className="logro-icono">{logro.icono}</span>
                <div className="logro-info">
                  <span className="logro-nombre">{logro.nombre}</span>
                  <span className="logro-desc">{logro.descripcion}</span>
                  {logro.desbloqueado && logro.fecha && (
                    <span className="logro-fecha">Obtenido: {logro.fecha}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PerfilPage;
