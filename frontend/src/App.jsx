import React, { useState, useEffect } from 'react';
import './App.css'; 

// IMPORTANTE: Use a URL local para testar antes do deploy da Function!
// Se o func start estiver rodando localmente, use:
const API_URL = 'http://localhost:7071/api/GetObrasFunction'; 

function App() {
  const [obras, setObras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Função para carregar os dados da Azure Function
    const fetchObras = async () => {
      try {
        const response = await fetch(API_URL);

        // Verifica se a resposta HTTP é 200 OK
        if (!response.ok) {
          throw new Error(`Erro HTTP! Status: ${response.status}`);
        }

        const data = await response.json();
        setObras(data);
      } catch (err) {
        console.error("Erro ao carregar obras:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchObras();
  }, []); // O array vazio garante que o efeito rode apenas uma vez

  if (loading) {
    return <h1 className="loading-message">Carregando Galeria...</h1>;
  }

  if (error) {
    return <h1 className="error-message">Erro ao buscar obras: {error}. Sua Azure Function está rodando?</h1>;
  }

  return (
    <div className="gallery-container">
      <header className="gallery-header">
        <h1>🖼️ Galeria de Artes Online </h1>
      </header>
      <div className="obras-list">
        {/* Mapeia a lista de obras e cria um card para cada uma */}
        {obras.length > 0 ? (
          obras.map((obra) => (
            <div key={obra.Nome} className="obra-card">
              <img src={obra.URLImagem} alt={obra.Nome} className="obra-image" />
              <div className="obra-details">
                <h2 className="obra-title">{obra.Nome}</h2>
                <p className="obra-artist">Artista: **{obra.Artista}**</p>
                <p className="obra-description">{obra.Descricao}</p>
              </div>
            </div>
          ))
        ) : (
          <h1 className="loading-message">Nenhuma obra encontrada. O DB está vazio?</h1>
        )}
      </div>
    </div>
  );
}

export default App;