import { useState, useRef, useEffect } from 'react';
import ChatBubble from '../components/ChatBubble';
import ChatInput from '../components/ChatInput';
import { preguntarAlChef, listarConversaciones, obtenerHistorialConversacion, eliminarConversacion } from '../services/api';
import './ChatPage.css';

const sugerencias = [
  { texto: 'Quiero aprender a hacer sushi', emoji: '🍣' },
  { texto: 'Enséñame a hacer pasta carbonara auténtica', emoji: '🍝' },
  { texto: 'Tengo pollo y verduras, qué cocino?', emoji: '🍗' },
  { texto: 'Quiero impresionar con un postre francés', emoji: '🍰' },
  { texto: 'Enséñame la técnica de flamear', emoji: '🔥' },
  { texto: 'Quiero cocinar algo de Marruecos', emoji: '🇲🇦' },
];

function ChatPage({ usuario, onAbrirCatalogo, onLogout, preguntaInicial }) {
  const bienvenida = {
    texto: `¡Benvenuto, **${usuario.nombre}**! 👨‍🍳 Soy el **Chef Vittorio**, tu mentor personal de cocina internacional.\n\nPuedo enseñarte recetas paso a paso, técnicas profesionales, o ayudarte a cocinar con lo que tengas en tu refrigerador.\n\n¿Qué te gustaría aprender hoy? 🔥`,
    esUsuario: false,
  };

  const [mensajes, setMensajes] = useState([bienvenida]);
  const [conversacionId, setConversacionId] = useState(null);
  const [conversaciones, setConversaciones] = useState([]);
  const [sidebarAbierta, setSidebarAbierta] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [preguntaProcesada, setPreguntaProcesada] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes]);

  useEffect(() => {
    cargarConversaciones();
  }, []);

  useEffect(() => {
    if (preguntaInicial && preguntaInicial !== preguntaProcesada) {
      setPreguntaProcesada(preguntaInicial);
      setTimeout(() => {
        handleEnviar(preguntaInicial);
      }, 100);
    }
  }, [preguntaInicial, preguntaProcesada]);

  const cargarConversaciones = async () => {
    try {
      const data = await listarConversaciones();
      setConversaciones(data);
    } catch (error) {
      console.error('Error cargando conversaciones:', error);
    }
  };

  const handleNuevaConversacion = () => {
    setConversacionId(null);
    setMensajes([bienvenida]);
    setSidebarAbierta(false);
  };

  const handleCargarConversacion = async (convId) => {
    try {
      const historial = await obtenerHistorialConversacion(convId);
      const mensajesCargados = historial.map((m) => ({
        texto: m.content,
        esUsuario: m.role === 'user',
      }));
      setConversacionId(convId);
      setMensajes([bienvenida, ...mensajesCargados]);
      setSidebarAbierta(false);
    } catch (error) {
      console.error('Error cargando conversación:', error);
    }
  };

  const handleEliminarConversacion = async (convId, e) => {
    e.stopPropagation();
    try {
      await eliminarConversacion(convId);
      setConversaciones((prev) => prev.filter((c) => c.id !== convId));
      if (conversacionId === convId) {
        handleNuevaConversacion();
      }
    } catch (error) {
      console.error('Error eliminando conversación:', error);
    }
  };

  const handleEnviar = async (texto) => {
    const nuevoMensaje = { texto, esUsuario: true };
    setMensajes((prev) => [...prev, nuevoMensaje]);
    setCargando(true);

    try {
      const data = await preguntarAlChef(texto, conversacionId);

      if (!conversacionId) {
        setConversacionId(data.conversacion_id);
        cargarConversaciones();
      }

      setMensajes((prev) => [
        ...prev,
        { texto: data.respuesta, esUsuario: false },
      ]);
    } catch (error) {
      setMensajes((prev) => [
        ...prev,
        {
          texto: 'Disculpa, mi cocina tuvo un problema técnico. Verifica que el backend esté corriendo en localhost:8000.',
          esUsuario: false,
        },
      ]);
    } finally {
      setCargando(false);
    }
  };

  const mostrarSugerencias = mensajes.length === 1 && !cargando;

  return (
    <div className="chat-layout">
      <div className={`sidebar ${sidebarAbierta ? 'abierta' : ''}`}>
        <div className="sidebar-header">
          <h2>Mis Chats</h2>
          <button className="btn-nueva-conv" onClick={handleNuevaConversacion}>
            + Nuevo Chat
          </button>
        </div>
        <div className="sidebar-lista">
          {conversaciones.length === 0 ? (
            <p className="sidebar-vacia">No tienes conversaciones aún</p>
          ) : (
            conversaciones.map((c) => (
              <div
                key={c.id}
                className={`sidebar-item ${conversacionId === c.id ? 'activo' : ''}`}
                onClick={() => handleCargarConversacion(c.id)}
              >
                <div className="sidebar-item-info">
                  <span className="sidebar-item-titulo">{c.titulo}</span>
                  <span className="sidebar-item-fecha">{c.fecha}</span>
                </div>
                <button
                  className="sidebar-item-delete"
                  onClick={(e) => handleEliminarConversacion(c.id, e)}
                >
                  ✕
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="chat-page">
        <header className="chat-header">
          <div className="header-left">
            <button className="btn-sidebar" onClick={() => setSidebarAbierta(!sidebarAbierta)}>
              ☰
            </button>
            <div className="header-logo">
              <span>V</span>
            </div>
            <div className="header-info">
              <h1>El Chef Mundial</h1>
              <p>Chef Vittorio · Cocina de los 5 continentes</p>
            </div>
          </div>
          <div className="header-actions">
            <button className="btn-catalogo" onClick={onAbrirCatalogo}>
              📖 Catálogo
            </button>
            <button className="btn-logout" onClick={onLogout}>
              Salir
            </button>
          </div>
        </header>

        <div className="chat-messages">
          {mensajes.map((msg, index) => (
            <ChatBubble
              key={index}
              mensaje={msg.texto}
              esUsuario={msg.esUsuario}
            />
          ))}

          {mostrarSugerencias && (
            <div className="sugerencias">
              <p className="sugerencias-titulo">Elige un tema o escribe tu pregunta:</p>
              <div className="sugerencias-grid">
                {sugerencias.map((s, i) => (
                  <button
                    key={i}
                    className="sugerencia-btn"
                    onClick={() => handleEnviar(s.texto)}
                  >
                    <span className="sugerencia-emoji">{s.emoji}</span>
                    <span className="sugerencia-texto">{s.texto}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {cargando && (
            <div className="typing-indicator">
              <div className="bubble-avatar chef-avatar">
                <span>V</span>
              </div>
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <ChatInput onEnviar={handleEnviar} cargando={cargando} />

        <footer className="chat-footer">
          <p>Chef Vittorio · Cocina internacional de los 5 continentes · Powered by AI</p>
        </footer>
      </div>

      {sidebarAbierta && (
        <div className="sidebar-overlay" onClick={() => setSidebarAbierta(false)}></div>
      )}
    </div>
  );
}

export default ChatPage;
