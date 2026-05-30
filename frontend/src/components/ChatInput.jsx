import { useState } from 'react';
import './ChatInput.css';

function ChatInput({ onEnviar, cargando }) {
  const [texto, setTexto] = useState('');

  const handleEnviar = () => {
    if (texto.trim() === '' || cargando) return;
    onEnviar(texto);
    setTexto('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleEnviar();
    }
  };

  return (
    <div className="chat-input-container">
      <div className="input-wrapper">
        <input
          type="text"
          className="chat-input"
          placeholder="Pregúntale al Chef Vittorio..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={cargando}
        />
        <button
          className="chat-send-btn"
          onClick={handleEnviar}
          disabled={cargando || texto.trim() === ''}
        >
          {cargando ? (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" strokeDasharray="30 60" strokeLinecap="round">
                <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
              </circle>
            </svg>
          ) : (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;
