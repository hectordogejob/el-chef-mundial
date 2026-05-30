import { useState } from 'react';
import './AuthPage.css';

function LoginPage({ onLogin, onIrARegistro }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async () => {
    if (!email || !password) {
      setError('Completa todos los campos');
      return;
    }
    setError('');
    setCargando(true);
    try {
      await onLogin(email, password);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión');
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
        <p className="auth-subtitle">Inicia sesión para cocinar con el Chef Vittorio</p>

        {error && <div className="auth-error">{error}</div>}

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
            placeholder="Tu contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={cargando}
          />
        </div>

        <button
          className="auth-btn"
          onClick={handleSubmit}
          disabled={cargando}
        >
          {cargando ? 'Entrando...' : 'Iniciar Sesión'}
        </button>

        <p className="auth-link">
          ¿No tienes cuenta?{' '}
          <span onClick={onIrARegistro}>Regístrate aquí</span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
