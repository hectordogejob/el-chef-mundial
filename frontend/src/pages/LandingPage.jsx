import './LandingPage.css';

function LandingPage({ onIrALogin, onIrARegistro }) {
  return (
    <div className="landing">
      <nav className="landing-nav">
        <div className="landing-nav-logo">
          <div className="nav-logo-icon">V</div>
          <span>El Chef Mundial</span>
        </div>
        <div className="landing-nav-btns">
          <button className="nav-btn-login" onClick={onIrALogin}>Iniciar Sesión</button>
          <button className="nav-btn-registro" onClick={onIrARegistro}>Registrarse Gratis</button>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-badge">👨‍🍳 Impulsado por Inteligencia Artificial</div>
        <h1>Tu Chef Personal de<br /><span className="hero-gold">Cocina Internacional</span></h1>
        <p className="hero-sub">Aprende a cocinar platillos de los 5 continentes con el Chef Vittorio, tu mentor personal con inteligencia artificial que se adapta a ti.</p>
        <div className="hero-btns">
          <button className="hero-btn-primary" onClick={onIrARegistro}>Empezar Gratis</button>
          <button className="hero-btn-secondary" onClick={onIrALogin}>Ya tengo cuenta</button>
        </div>
        <p className="hero-note">Sin tarjeta de crédito · 3 consultas diarias gratis</p>
      </section>

      <section className="features">
        <h2>¿Qué puedes hacer?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-icon">🤖</span>
            <h3>Chef con IA</h3>
            <p>Pregúntale cualquier cosa sobre cocina. Te responde como un chef profesional con técnicas, tips y recetas paso a paso.</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">🌍</span>
            <h3>34 Recetas de 6 Continentes</h3>
            <p>Desde sushi japonés hasta mole poblano, pasando por curry tailandés y tagine marroquí. Cocina del mundo entero.</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">📝</span>
            <h3>Lista de Ingredientes</h3>
            <p>Genera tu lista de compras automáticamente y compártela por WhatsApp. Nunca olvides un ingrediente.</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">🎮</span>
            <h3>Gamificación</h3>
            <p>Sube de nivel: de Aprendiz a Master Chef. Gana XP, desbloquea logros y mantén tu racha diaria.</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">❤️</span>
            <h3>Favoritos</h3>
            <p>Guarda tus recetas favoritas y accede a ellas con un clic. Tu colección personal de platillos.</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">💬</span>
            <h3>Memoria Inteligente</h3>
            <p>El Chef recuerda tus conversaciones anteriores. Retoma donde te quedaste sin repetir nada.</p>
          </div>
        </div>
      </section>

      <section className="como-funciona">
        <h2>¿Cómo funciona?</h2>
        <div className="pasos-grid">
          <div className="paso-landing">
            <div className="paso-num">1</div>
            <h3>Regístrate gratis</h3>
            <p>Crea tu cuenta en 10 segundos. Solo necesitas email y contraseña.</p>
          </div>
          <div className="paso-landing">
            <div className="paso-num">2</div>
            <h3>Explora o pregunta</h3>
            <p>Navega el catálogo de recetas o pregúntale al Chef lo que quieras cocinar.</p>
          </div>
          <div className="paso-landing">
            <div className="paso-num">3</div>
            <p>Sigue los pasos, marca ingredientes y comparte tu lista de compras.</p>
            <h3>Cocina como profesional</h3>
          </div>
        </div>
      </section>

      <section className="pricing">
        <h2>Planes</h2>
        <div className="pricing-grid">
          <div className="plan-card">
            <h3>Gratis</h3>
            <p className="plan-precio">$0</p>
            <ul>
              <li>✅ 3 preguntas al Chef por día</li>
              <li>✅ Catálogo completo de recetas</li>
              <li>✅ Lista de ingredientes</li>
              <li>✅ Favoritos</li>
              <li>✅ Gamificación</li>
              <li>❌ Preguntas ilimitadas</li>
            </ul>
            <button className="plan-btn-free" onClick={onIrARegistro}>Empezar Gratis</button>
          </div>
          <div className="plan-card plan-premium">
            <div className="plan-popular">Más Popular</div>
            <h3>Premium 👑</h3>
            <p className="plan-precio">$49 <span>MXN/mes</span></p>
            <ul>
              <li>✅ Preguntas ILIMITADAS al Chef</li>
              <li>✅ Todo lo del plan gratis</li>
              <li>✅ Recetas exclusivas</li>
              <li>✅ Sin límites</li>
              <li>✅ Soporte prioritario</li>
              <li>✅ Badge Premium 👑</li>
            </ul>
            <button className="plan-btn-premium" onClick={onIrARegistro}>Hazte Premium</button>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="footer-cta">
          <h2>¿Listo para cocinar como profesional?</h2>
          <button className="hero-btn-primary" onClick={onIrARegistro}>Empezar Gratis Ahora</button>
        </div>
        <p className="footer-copy">© 2026 El Chef Mundial · Hecho con 🔥 por Chef Vittorio</p>
      </footer>
    </div>
  );
}

export default LandingPage;
