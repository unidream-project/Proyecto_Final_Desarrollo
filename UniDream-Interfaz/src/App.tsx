import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// 1. IMPORTAR LAS PÁGINAS QUE FALTABAN
import FrameInicio from './pages/FrameInicio';
import FrameAsistenteIA from './pages/FrameAsistenteIA';
import FrameCarreras from './pages/FrameCarreras';       // <--- Nuevo
import FrameUniversidades from './pages/FrameUniversidades'; // <--- Nuevo

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta principal */}
        <Route path="/" element={<FrameInicio />} /> 
        
        {/* Rutas secundarias */}
        <Route path="/inicio" element={<FrameInicio />} />
        <Route path="/asistente" element={<FrameAsistenteIA />} />
        
        {/* 2. AGREGAR LAS RUTAS NUEVAS PARA QUE LOS BOTONES FUNCIONEN */}
        <Route path="/carreras" element={<FrameCarreras />} />         {/* <--- Ahora el link funcionará */}
        <Route path="/universidades" element={<FrameUniversidades />} /> {/* <--- Ahora el link funcionará */}
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;