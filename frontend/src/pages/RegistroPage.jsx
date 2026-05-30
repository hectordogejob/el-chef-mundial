import { useState } from 'react';
import './AuthPage.css';

function RegistroPage({ onRegistro, onIrALogin }) {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmar, setConfirmar] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async () => {
    if (!nombre || !email || !password || !confirmar) {
      setError('Completa todos los campos');
      return;
    }
    if (password !== confirmar) {
      setError('Las contraseñas no coinciden');
      return;
    }
    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }
    setError('');
    setCargando(true);
    try {
      await onRegistro(nombre, email, password);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrarse');
    } finally {
      setCargando(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSubmit();
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">
          <span>V</span>
        </div>
        <h1>El Chef Mundial</h1>
        <p className="auth-subtitle">Crea tu cuenta y aprende a cocinar como profesional</p>

        {error && <div className="auth-error">{error}</div>}

        <div className="auth-field">
          <label>Nombre</label>
          <input
            type="text"
            placeholder="Tu nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={cargando}
          />
        </div>

        <div className="auth-field">
          <label>Email</label>
          <input
            type="email"
            placeholder="tu@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={cargando}
          />
        </div>

        <div className="auth-field">
          <label>Contraseña</label>
          <input
            type="password"
            placeholder="Mínimo 6 caracteres"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={cargando}
          />
        </div>

        <div className="auth-field">
          <label>Confirmar Contraseña</label>
          <input
            type="password"
            placeholder="Repite tu contraseña"
            value={confirmar}
            onChange={(e) => setConfirmar(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={cargando}
          />
        </div>

        <button
          className="auth-btn"
          onClick={handleSubmit}
          disabled={cargando}
        >
          {cargando ? 'Creando cuenta...' : 'Crear Cuenta'}
        </button>

        <p className="auth-link">
          ¿Ya tienes cuenta?{' '}
          <span onClick={onIrALogin}>Inicia sesión</span>
        </p>
      </div>
    </div>
  );
}

export default RegistroPage;
