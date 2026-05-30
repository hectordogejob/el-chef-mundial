import { useState, useEffect } from 'react';
import { obtenerIngredientes } from '../services/api';
import './ListaComprasPage.css';

function ListaComprasPage({ platilloId, platilloNombre, onVolver }) {
  const [datos, setDatos] = useState(null);
  const [checkeados, setCheckeados] = useState({});
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      try {
        const data = await obtenerIngredientes(platilloId);
        setDatos(data);
      } catch (error) {
        console.error('Error cargando ingredientes:', error);
      } finally {
        setCargando(false);
      }
    };
    cargar();
  }, [platilloId]);

  const toggleCheck = (index) => {
    setCheckeados((prev) => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const totalCheckeados = Object.values(checkeados).filter(Boolean).length;
  const totalIngredientes = datos?.ingredientes?.length || 0;

  const generarTextoLista = () => {
    if (!datos || !datos.ingredientes) return '';
    let texto = `Lista de compras: ${datos.platillo}\n`;
    texto += `Para ${datos.porciones} porciones\n\n`;
    datos.ingredientes.forEach((ing) => {
      const check = checkeados[datos.ingredientes.indexOf(ing)] ? '✅' : '⬜';
      texto += `${check} ${ing.cantidad} - ${ing.nombre}`;
      if (ing.notas) texto += ` (${ing.notas})`;
      texto += '\n';
    });
    texto += '\nGenerado por El Chef Mundial';
    return texto;
  };

  const copiarLista = () => {
    navigator.clipboard.writeText(generarTextoLista());
    alert('Lista copiada al portapapeles');
  };

  const compartirWhatsApp = () => {
    const texto = encodeURIComponent(generarTextoLista());
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  };

  if (cargando) {
    return (
      <div className="lista-page">
        <div className="lista-cargando">Cargando ingredientes...</div>
      </div>
    );
  }

  if (!datos || !datos.tiene_ingredientes) {
    return (
      <div className="lista-page">
        <header className="lista-header">
          <button className="btn-volver-lista" onClick={onVolver}>← Volver</button>
          <h1>{platilloNombre}</h1>
        </header>
        <div className="lista-vacia">
          <p>Este platillo no tiene ingredientes detallados en la base de datos.</p>
          <p>Pidele la receta completa al <strong>Chef Vittorio</strong> en el chat.</p>
          <button className="btn-ir-chef" onClick={onVolver}>← Volver al catalogo</button>
        </div>
      </div>
    );
  }

  return (
    <div className="lista-page">
      <header className="lista-header">
        <button className="btn-volver-lista" onClick={onVolver}>← Volver</button>
        <div className="lista-header-info">
          <h1>{datos.platillo}</h1>
          <p>Para {datos.porciones} porciones · {totalCheckeados}/{totalIngredientes} comprados</p>
        </div>
      </header>

      <div className="lista-progreso">
        <div
          className="lista-progreso-bar"
          style={{ width: totalIngredientes > 0 ? `${(totalCheckeados / totalIngredientes) * 100}%` : '0%' }}
        ></div>
      </div>

      <div className="lista-items">
        {datos.ingredientes.map((ing, index) => (
          <div
            key={index}
            className={`lista-item ${checkeados[index] ? 'comprado' : ''}`}
            onClick={() => toggleCheck(index)}
          >
            <div className="lista-check">
              {checkeados[index] ? '✅' : '⬜'}
            </div>
            <div className="lista-item-info">
              <span className="lista-item-nombre">{ing.nombre}</span>
              <span className="lista-item-cantidad">{ing.cantidad}</span>
              {ing.notas && <span className="lista-item-notas">{ing.notas}</span>}
            </div>
          </div>
        ))}
      </div>

      <div className="lista-acciones">
        <button className="btn-copiar" onClick={copiarLista}>
          📋 Copiar lista
        </button>
        <button className="btn-whatsapp" onClick={compartirWhatsApp}>
          📱 Compartir por WhatsApp
        </button>
      </div>
    </div>
  );
}

export default ListaComprasPage;
