import { useEffect, useState, useCallback } from "react";
import "./App.css";
import TeamSelect from "./componets/Team_Select.js";
import PlayerCard from "./componets/Player_Card.js";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const API_BASE_URL = "http://localhost:8000/api";

function App() {
  const [teams, setTeams] = useState([]);
  const [predicciones, setPredicciones] = useState(null);
  const [selected1, setSelected1] = useState(null);
  const [selected2, setSelected2] = useState(null);
  const [jugadores1, setJugadores1] = useState([]);
  const [jugadores2, setJugadores2] = useState([]);
  const [isModalTeam, setIsModalTeam] = useState(false);
  const [targetTeam, setTargetTeam] = useState(null);
  const [agentes, setAgentes] = useState([]);
  const [targetPlayer, setTargetPlayer] = useState(null);
  const [selectedAgents, setSelectedAgents] = useState({});
  const [isModalAgent, setIsModalAgent] = useState(false);
  const [maps, setMaps] = useState([]);
  const [currentMap, setCurrentMap] = useState(null);
  const [equipoQueEmpieza, setEquipoQueEmpieza] = useState('equipo1');
  const [showSettingsMenu, setShowSettingsMenu] = useState(false);
  const [toggleStates, setToggleStates] = useState({});

  const fetchData = useCallback(async (url, setter) => {
    try {
      const res = await fetch(url);
      const data = await res.json();
      setter(data);
    } catch (err) {
      console.error(`Error cargando datos de ${url}:`, err);
    }
  }, []);

  useEffect(() => {
    fetchData(`${API_BASE_URL}/teams/`, setTeams);
    fetchData(`${API_BASE_URL}/agentes/`, setAgentes);
    fetchData(`${API_BASE_URL}/maps/`, setMaps);
  }, [fetchData]);

  useEffect(() => {
    if (maps.length > 0) {
      setCurrentMap(maps[0]);
    }
  }, [maps]);

  const fetchJugadores = useCallback(async (teamId, setJugadores) => {
    if (!teamId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/teams/${teamId}/jugadores/`);
      const data = await res.json();
      setJugadores(data);
      setSelectedAgents({});
    } catch (err) {
      console.error("Error cargando jugadores:", err);
    }
  }, []);

  useEffect(() => {
    fetchJugadores(selected1, setJugadores1);
  }, [selected1, fetchJugadores]);

  useEffect(() => {
    fetchJugadores(selected2, setJugadores2);
  }, [selected2, fetchJugadores]);

  const handleSelect = (team) => {
    if (targetTeam === "equipo1") {
      setSelected1(team.id);
      setPredicciones(null);
    } else if (targetTeam === "equipo2") {
      setSelected2(team.id);
      setPredicciones(null);
    }
    setIsModalTeam(false);
  };

  const handleAgentSelect = (agent) => {
    setSelectedAgents((prev) => ({
      ...prev,
      [targetPlayer]: agent,
    }));
    setIsModalAgent(false);
    setPredicciones(null);
  };

  const selectedTeam1 = teams.find((t) => t.id === selected1);
  const selectedTeam2 = teams.find((t) => t.id === selected2);

  const handlePredicciones = async () => {
    const payload = {
      jugadores1: jugadores1.map((j) => j.id),
      jugadores2: jugadores2.map((j) => j.id),
      equipo1: selected1,
      equipo2: selected2,
      mapa: currentMap ? currentMap.nombre : null,
      agentes: Object.entries(selectedAgents).map(([nombre_jugador, agent]) => ({
        nombre_jugador,
        nombre_agente: agent.nombre,
      })),
      equipoQueEmpieza,
      ajustes: toggleStates,
    };

    try {
      const res = await fetch(`${API_BASE_URL}/predicciones/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setPredicciones(data);
    } catch (err) {
      console.error("Error al obtener predicciones:", err);
    }
  };

  const isPredictionReady =
    selected1 &&
    selected2 &&
    currentMap &&
    jugadores1.length > 0 &&
    jugadores2.length > 0 &&
    jugadores1.every((j) => selectedAgents[j.nombre_jugador]) &&
    jugadores2.every((j) => selectedAgents[j.nombre_jugador]);

  const mapSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    afterChange: (index) => {
      setCurrentMap(maps[index]);
    },
  };

  const getHighlight = (player, teamPredictions) => {
    if (!teamPredictions || teamPredictions.length === 0) return null;

    const scores = teamPredictions.map((p) => p.score);
    const maxScore = Math.max(...scores);
    const minScore = Math.min(...scores);

    const playerScore = teamPredictions.find(
      (p) => p.nombre === player.nombre_jugador
    )?.score;

    if (playerScore === maxScore) return "high";
    if (playerScore === minScore) return "low";
    return null;
  };

  return (
    <div className="app-container">
    
      <style>
       
      </style>
      <div className="zones-container">
        <div className="team-zone">
          <div className="agent-grid">
            <TeamSelect
              selectedTeam={selectedTeam1}
              onClick={() => {
                setTargetTeam("equipo1");
                setIsModalTeam(true);
              }}
            />
            {jugadores1.map((jugador) => (
              <PlayerCard
                key={`e1-${jugador.nombre_jugador}`}
                jugador={jugador}
                selectedAgent={selectedAgents[jugador.nombre_jugador] || null}
                onClick={() => {
                  setTargetPlayer(jugador.nombre_jugador);
                  setIsModalAgent(true);
                }}
                highlight={getHighlight(jugador, predicciones?.equipo1)}
              />
            ))}
          </div>
        </div>
        <div className="map-container">
          {maps.length > 0 && (
            <Slider {...mapSettings}>
              {maps.map((mapa) => (
                <img
                  key={mapa.id}
                  src={mapa.imagen_mapa}
                  alt={mapa.nombre}
                  className="map-img"
                />
              ))}
            </Slider>
          )}
        </div>
        <div className="team-zone">
          <div className="agent-grid">
            <TeamSelect
              selectedTeam={selectedTeam2}
              onClick={() => {
                setTargetTeam("equipo2");
                setIsModalTeam(true);
              }}
            />
            {jugadores2.map((jugador) => (
              <PlayerCard
                key={jugador.nombre_jugador}
                jugador={jugador}
                selectedAgent={selectedAgents[jugador.nombre_jugador] || null}
                onClick={() => {
                  setTargetPlayer(jugador.nombre_jugador);
                  setIsModalAgent(true);
                }}
                highlight={getHighlight(jugador, predicciones?.equipo2)}
              />
            ))}
          </div>
        </div>

        {isModalTeam && (
          <div className="modal-overlay">
            <div className="modal">
              <h3 style={{ color: "white", fontFamily: "Verdana, sans-serif" }}>
                Selecciona tu equipo
              </h3>
              <div className="team-grid">
                {teams.filter((team) => {
                  if (targetTeam === "equipo1") {
                    return team.id !== selected2;
                  } else if (targetTeam === "equipo2") {
                    return team.id !== selected1;
                  }
                  return true;
                }).map((team) => (
                  <div
                    key={team.id}
                    className="team-card"
                    onClick={() => handleSelect(team)}
                  >
                    <img
                      src={team.imagen_equipo}
                      alt={team.nombre}
                      className="team-card-img"
                    />
                    <span className="team-name">{team.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {isModalAgent && (
          <div className="modal-overlay-agent">
            <div className="modal-agent">
              <div className="agent-grid">
                {(() => {
                  let jugadoresEquipo = [];
                  if (jugadores1.some(j => j.nombre_jugador === targetPlayer)) {
                    jugadoresEquipo = jugadores1;
                  } else if (jugadores2.some(j => j.nombre_jugador === targetPlayer)) {
                    jugadoresEquipo = jugadores2;
                  }
                  const agentesSeleccionados = jugadoresEquipo
                    .filter(j => j.nombre_jugador !== targetPlayer)
                    .map(j => selectedAgents[j.nombre_jugador]?.nombre)
                    .filter(Boolean);
                  return agentes
                    .filter(agente => !agentesSeleccionados.includes(agente.nombre))
                    .map((agente) => (
                      <div
                        key={agente.id}
                        className="agent-card"
                        onClick={() => handleAgentSelect(agente)}
                      >
                        <img
                          src={agente.imagen_personaje}
                          alt={agente.nombre}
                          className="agent-card-img"
                        />
                        <span className="agent-name">{agente.name}</span>
                      </div>
                    ));
                })()}
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="dataContainer" style={{ position: 'relative' }}>
        <button
          onClick={() => setShowSettingsMenu(prev => !prev)}
          style={{
            position: 'absolute',
            top: '8px',
            right: '8px',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            fontSize: '18px',
            color: '#fff'
          }}
          aria-label="Toggle settings menu"
        >
          ⋮
        </button>
        
        {showSettingsMenu && (
          <div
            style={{
              marginTop: '16px',
              backgroundColor: '#f0f0f0',
              color: '#000',
              padding: '16px',
              borderRadius: '8px',
            }}
          >
            <h4>Configuración:</h4>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {[
                'Kills por ronda',
                'Muerte por ronda',
                'Mejor mapa',
                'Peor mapa',  
                'Rol recomendado',
                'Coste de kill',
                'Primera kill de la ronda',
                'Composición',
                'Racha',
                'Counters',
              ].map((label, index) => {
                const id = `setting-${index}`;

                return (
                  <div
                    key={label}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                    }}
                  >
                    <label htmlFor={id}>{label}</label>

                    <div className="switch">
                      <input
                        id={id}
                        type="checkbox"
                        checked={toggleStates[label] === 1}
                        onChange={(e) =>
                          setToggleStates((prev) => ({
                            ...prev,
                            [label]: e.target.checked ? 1 : 0,
                          }))
                        }
                      />
                      <span className="slider"></span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
        
        {!showSettingsMenu && (
          <>
            {currentMap && (
              <h2 aria-label={`Selected map: ${currentMap.nombre}`}>
                {currentMap.nombre}
              </h2>
            )}

            <div style={{ margin: '2px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <label htmlFor="quien-empieza" style={{ fontWeight: 'bold' }}>¿Quién empieza?</label>
              <select
                id="quien-empieza"
                value={equipoQueEmpieza}
                onChange={e => {
                  setEquipoQueEmpieza(e.target.value);
                  setPredicciones(null);
                }}
                style={{ borderRadius: '6px' }}
              >
                <option value="equipo1">{selectedTeam1 ? selectedTeam1.nombre_equipo : 'Equipo 1'}</option>
                <option value="equipo2">{selectedTeam2 ? selectedTeam2.nombre_equipo : 'Equipo 2'}</option>
              </select>
            </div>

            {isPredictionReady && (
              <button onClick={handlePredicciones}>Calcular Predicciones</button>
            )}
          </>
        )}

        {!showSettingsMenu && predicciones && (
          <div className="predicciones-resultado">
            {predicciones.error ? (
              <p>Error: {predicciones.error}</p>
            ) : (
              <div>
                <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
                  <div>
                    <h4>{selectedTeam1 ? selectedTeam1.nombre_equipo : 'Equipo 1'}</h4>
                    <span className={`tipo-composicion tipo-${predicciones.tipo_composicion_equipo1}`}>{predicciones.tipo_composicion_equipo1}</span>
                    <div className="porcentaje-victoria" style={{ marginBottom: '8px' }}>
                      {selectedTeam1 ? selectedTeam1.nombre_equipo : 'Equipo 1'}<br />
                      <span style={{ fontWeight: 'bold', color: (predicciones.porcentaje_victoria_equipo1 >= predicciones.porcentaje_victoria_equipo2 ? '#43a047' : '#e53935') }}>
                        {predicciones.porcentaje_victoria_equipo1} %
                      </span>
                    </div>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {predicciones.equipo1 &&
                        predicciones.equipo1
                          .map((p, idx) => (
                            <li key={p.nombre} style={{ marginBottom: '8px' }}>
                              <strong>{idx + 1}.</strong> {p.nombre} <span style={{ color: '#888' }}>({p.score})</span>
                            </li>
                          ))}
                    </ul>
                  </div>
                  <div>
                    <h4>{selectedTeam2 ? selectedTeam2.nombre_equipo : 'Equipo 2'}</h4>
                    <span className={`tipo-composicion tipo-${predicciones.tipo_composicion_equipo2}`}>{predicciones.tipo_composicion_equipo2}</span>
                    <div className="porcentaje-victoria" style={{ marginBottom: '8px' }}>
                      {selectedTeam2 ? selectedTeam2.nombre_equipo : 'Equipo 2'}<br />
                      <span style={{ fontWeight: 'bold', color: (predicciones.porcentaje_victoria_equipo2 > predicciones.porcentaje_victoria_equipo1 ? '#43a047' : '#e53935') }}>
                        {predicciones.porcentaje_victoria_equipo2} %
                      </span>
                    </div>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {predicciones.equipo2 &&
                        predicciones.equipo2
                          .map((p, idx) => (
                            <li key={p.nombre} style={{ marginBottom: '8px' }}>
                              <strong>{idx + 1}.</strong> {p.nombre} <span style={{ color: '#888' }}>({p.score})</span>
                            </li>
                          ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
