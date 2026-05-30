import ReactMarkdown from 'react-markdown';
import './ChatBubble.css';

function ChatBubble({ mensaje, esUsuario }) {
  return (
    <div className={`chat-bubble ${esUsuario ? 'usuario' : 'chef'}`}>
      {!esUsuario && (
        <div className="bubble-avatar chef-avatar">
          <span>V</span>
        </div>
      )}
      <div className={`bubble-content ${esUsuario ? 'usuario-content' : 'chef-content'}`}>
        {esUsuario ? (
          <p className="bubble-text-plain">{mensaje}</p>
        ) : (
          <div className="bubble-markdown">
            <ReactMarkdown>{mensaje}</ReactMarkdown>
          </div>
        )}
      </div>
      {esUsuario && (
        <div className="bubble-avatar usuario-avatar">
          <span>Tú</span>
        </div>
      )}
    </div>
  );
}

export default ChatBubble;
