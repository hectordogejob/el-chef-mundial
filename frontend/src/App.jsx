import { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import RegistroPage from './pages/RegistroPage';
import ChatPage from './pages/ChatPage';
import CatalogoPage from './pages/CatalogoPage';
import ListaComprasPage from './pages/ListaComprasPage';
import { loginUsuario, registrarUsuario } from './services/api';
import DetallePlatilloPage from './pages/DetallePlatilloPage';

function App() {
  const [usuario, setUsuario] = useState(null);
  const [vista, setVista] = useState('login');
  const [preguntaDesdeCategoria, setPreguntaDesdeCategoria] = useState(null);
  const [listaCompras, setListaCompras] = useState(null);
  const [detallePlatillo, setDetallePlatillo] = useState(null);

  useEffect(() => {
    const guardado = localStorage.getItem('chef_usuario');
    if (guardado) {
      setUsuario(JSON.parse(guardado));
      setVista('chat');
    }
  }, []);

  const handleLogin = async (email, password) => {
    const data = await loginUsuario(email, password);
    const userData = {
      token: data.access_token,
      ...data.usuario
    };
    localStorage.setItem('chef_usuario', JSON.stringify(userData));
    setUsuario(userData);
    setVista('chat');
  };

  const handleRegistro = async (nombre, email, password) => {
    const data = await registrarUsuario(nombre, email, password);
    const userData = {
      token: data.access_token,
      ...data.usuario
    };
    localStorage.setItem('chef_usuario', JSON.stringify(userData));
    setUsuario(userData);
    setVista('chat');
  };

  const handleLogout = () => {
    localStorage.removeItem('chef_usuario');
    setUsuario(null);
    setVista('login');
  };

  const handlePreguntarPlatillo = (pregunta) => {
    setPreguntaDesdeCategoria(pregunta);
    setVista('chat');
  };

  const handleVerListaCompras = (platilloId, platilloNombre) => {
    setListaCompras({ id: platilloId, nombre: platilloNombre });
    setVista('lista');
  };
const handleVerDetalle = (platilloId) => {
    setDetallePlatillo(platilloId);
    setVista('detalle');
};
  if (!usuario) {
    return vista === 'login' ? (
      <LoginPage
        onLogin={handleLogin}
        onIrARegistro={() => setVista('registro')}
      />
    ) : (
      <RegistroPage
        onRegistro={handleRegistro}
        onIrALogin={() => setVista('login')}
      />
    );
  }
if (vista === 'detalle' && detallePlatillo) {
    return (
      <DetallePlatilloPage
        platilloId={detallePlatillo}
        onVolver={() => setVista('catalogo')}
        onPreguntarChef={handlePreguntarPlatillo}
        onVerIngredientes={handleVerListaCompras}
      />
    );
}
  if (vista === 'lista' && listaCompras) {
    return (
      <ListaComprasPage
        platilloId={listaCompras.id}
        platilloNombre={listaCompras.nombre}
        onVolver={() => setVista('catalogo')}
      />
    );
  }

  if (vista === 'catalogo') {
    return (
      <CatalogoPage
        onVolverAlChat={() => setVista('chat')}
        onPreguntarPlatillo={handlePreguntarPlatillo}
        onVerListaCompras={handleVerListaCompras}
        onVerDetalle={handleVerDetalle}
      />
    );
  }

  return (
    <ChatPage
      usuario={usuario}
      onAbrirCatalogo={() => setVista('catalogo')}
      onLogout={handleLogout}
      preguntaInicial={preguntaDesdeCategoria}
    />
  );
}

export default App;
