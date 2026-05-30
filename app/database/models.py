from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Continente(Base):
    __tablename__ = "Continentes"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)
    paises = relationship("Pais", back_populates="continente")


class Pais(Base):
    __tablename__ = "Paises"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ContinenteId = Column(Integer, ForeignKey("Continentes.Id"), nullable=False)
    Nombre = Column(String(100), nullable=False)
    continente = relationship("Continente", back_populates="paises")
    cocinas = relationship("Cocina", back_populates="pais")


class Cocina(Base):
    __tablename__ = "Cocinas"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PaisId = Column(Integer, ForeignKey("Paises.Id"), nullable=False)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(500), nullable=True)
    pais = relationship("Pais", back_populates="cocinas")
    platillos = relationship("Platillo", back_populates="cocina")


class CategoriaPlatillo(Base):
    __tablename__ = "CategoriaPlatillo"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)


class NivelDificultad(Base):
    __tablename__ = "NivelDificultad"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)
    Descripcion = Column(String(200), nullable=True)


class Tecnica(Base):
    __tablename__ = "Tecnicas"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(500), nullable=False)
    NivelId = Column(Integer, ForeignKey("NivelDificultad.Id"), nullable=False)
    nivel = relationship("NivelDificultad")


class Utensilio(Base):
    __tablename__ = "Utensilios"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(300), nullable=True)
    Indispensable = Column(Boolean, default=False)


class Ingrediente(Base):
    __tablename__ = "Ingredientes"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Categoria = Column(String(50), nullable=True)


class Platillo(Base):
    __tablename__ = "Platillos"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    CocinaId = Column(Integer, ForeignKey("Cocinas.Id"), nullable=False)
    CategoriaId = Column(Integer, ForeignKey("CategoriaPlatillo.Id"), nullable=False)
    NivelId = Column(Integer, ForeignKey("NivelDificultad.Id"), nullable=False)
    Nombre = Column(String(200), nullable=False)
    Descripcion = Column(String(500), nullable=True)
    TiempoPreparacion = Column(String(50), nullable=True)
    Porciones = Column(Integer, nullable=True)
    Historia = Column(String(500), nullable=True)
    TipChefVittorio = Column(String(500), nullable=True)
    Imagen = Column(String(200), nullable=True)
    Activo = Column(Boolean, default=True)
    cocina = relationship("Cocina", back_populates="platillos")
    categoria = relationship("CategoriaPlatillo")
    nivel = relationship("NivelDificultad")
    ingredientes = relationship("PlatilloIngrediente", back_populates="platillo")
    utensilios = relationship("PlatilloUtensilio", back_populates="platillo")
    tecnicas = relationship("PlatilloTecnica", back_populates="platillo")
    pasos = relationship("PasoPlatillo", back_populates="platillo")


class PlatilloIngrediente(Base):
    __tablename__ = "PlatilloIngredientes"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlatilloId = Column(Integer, ForeignKey("Platillos.Id"), nullable=False)
    IngredienteId = Column(Integer, ForeignKey("Ingredientes.Id"), nullable=False)
    Cantidad = Column(String(50), nullable=False)
    Notas = Column(String(200), nullable=True)
    platillo = relationship("Platillo", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")


class PlatilloUtensilio(Base):
    __tablename__ = "PlatilloUtensilios"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlatilloId = Column(Integer, ForeignKey("Platillos.Id"), nullable=False)
    UtensilioId = Column(Integer, ForeignKey("Utensilios.Id"), nullable=False)
    Obligatorio = Column(Boolean, default=True)
    platillo = relationship("Platillo", back_populates="utensilios")
    utensilio = relationship("Utensilio")


class PlatilloTecnica(Base):
    __tablename__ = "PlatilloTecnicas"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlatilloId = Column(Integer, ForeignKey("Platillos.Id"), nullable=False)
    TecnicaId = Column(Integer, ForeignKey("Tecnicas.Id"), nullable=False)
    platillo = relationship("Platillo", back_populates="tecnicas")
    tecnica = relationship("Tecnica")


class PasoPlatillo(Base):
    __tablename__ = "PasosPlatillo"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlatilloId = Column(Integer, ForeignKey("Platillos.Id"), nullable=False)
    NumPaso = Column(Integer, nullable=False)
    Instruccion = Column(String(500), nullable=False)
    TipChef = Column(String(300), nullable=True)
    TiempoMinutos = Column(Integer, nullable=True)
    platillo = relationship("Platillo", back_populates="pasos")


class Usuario(Base):
    __tablename__ = "Usuarios"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Email = Column(String(200), nullable=False, unique=True)
    PasswordHash = Column(String(500), nullable=False)
    FechaRegistro = Column(DateTime, default=datetime.now)
    Activo = Column(Boolean, default=True)
    EsPremium = Column(Boolean, default=False)
    LimiteDiario = Column(Integer, default=3)
    conversaciones = relationship("Conversacion", back_populates="usuario")
    favoritos = relationship("Favorito", back_populates="usuario")


class Conversacion(Base):
    __tablename__ = "Conversaciones"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioId = Column(Integer, ForeignKey("Usuarios.Id"), nullable=False)
    Titulo = Column(String(200), nullable=False)
    FechaCreacion = Column(DateTime, default=datetime.now)
    Activa = Column(Boolean, default=True)
    usuario = relationship("Usuario", back_populates="conversaciones")
    mensajes = relationship("HistorialConversacion", back_populates="conversacion")


class HistorialConversacion(Base):
    __tablename__ = "HistorialConversaciones"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioId = Column(Integer, ForeignKey("Usuarios.Id"), nullable=False)
    ConversacionId = Column(Integer, ForeignKey("Conversaciones.Id"), nullable=True)
    Role = Column(String(20), nullable=False)
    Contenido = Column(String, nullable=False)
    Fecha = Column(DateTime, default=datetime.now)
    conversacion = relationship("Conversacion", back_populates="mensajes")


class Favorito(Base):
    __tablename__ = "Favoritos"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioId = Column(Integer, ForeignKey("Usuarios.Id"), nullable=False)
    PlatilloId = Column(Integer, ForeignKey("Platillos.Id"), nullable=False)
    FechaAgregado = Column(DateTime, default=datetime.now)
    usuario = relationship("Usuario", back_populates="favoritos")
    platillo = relationship("Platillo")
    __table_args__ = (
        UniqueConstraint('UsuarioId', 'PlatilloId', name='UQ_Usuario_Platillo'),
    )


class Nivel(Base):
    __tablename__ = "Niveles"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)
    XPMinimo = Column(Integer, nullable=False)
    XPMaximo = Column(Integer, nullable=False)
    Icono = Column(String(10), nullable=False)


class PerfilGamer(Base):
    __tablename__ = "PerfilGamer"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioId = Column(Integer, ForeignKey("Usuarios.Id"), nullable=False, unique=True)
    NivelId = Column(Integer, ForeignKey("Niveles.Id"), nullable=False, default=1)
    XP = Column(Integer, nullable=False, default=0)
    Racha = Column(Integer, nullable=False, default=0)
    MejorRacha = Column(Integer, nullable=False, default=0)
    PlatillosCocinados = Column(Integer, nullable=False, default=0)
    PreguntasAlChef = Column(Integer, nullable=False, default=0)
    UltimaActividad = Column(DateTime, nullable=True)
    nivel = relationship("Nivel")


class Logro(Base):
    __tablename__ = "Logros"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(300), nullable=False)
    Icono = Column(String(10), nullable=False)
    Condicion = Column(String(50), nullable=False)
    Valor = Column(Integer, nullable=False)


class UsuarioLogro(Base):
    __tablename__ = "UsuarioLogros"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioId = Column(Integer, ForeignKey("Usuarios.Id"), nullable=False)
    LogroId = Column(Integer, ForeignKey("Logros.Id"), nullable=False)
    FechaObtenido = Column(DateTime, default=datetime.now)
    logro = relationship("Logro")
    __table_args__ = (
        UniqueConstraint('UsuarioId', 'LogroId', name='UQ_Usuario_Logro'),
    )