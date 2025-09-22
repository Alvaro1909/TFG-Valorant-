import { useEffect, useState } from "react";
import "./App.css";
import TeamSelect from "./componets/Team_Select.js";
import PlayerCard from "./componets/Player_Card.js";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";


export default function App() {
  const [teams, setTeams] = useState([]);
  const [selected1, setSelected1] = useState(null);
  const [selected2, setSelected2] = useState(null);
  const [targetTeam, setTargetTeam] = useState(null);
  const [jugadores1, setJugadores1] = useState([]);
  const [jugadores2, setJugadores2] = useState([]);
  const [isModalTeam, setIsModalTeam] = useState(false);
  const [agentes, setAgentes] = useState([]);
  const [selectedAgents, setSelectedAgents] = useState({});
  const [isModalAgent, setIsModalAgent] = useState(false);
  const [maps, setMaps] = useState([]);
  const [currentMap, setCurrentMap] = useState(maps[0] || null);


  useEffect(() => {
    fetch("/api/teams/")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch((err) => console.error("Error cargando equipos:", err));
  }, []);

  useEffect(() => {
    fetch("/api/agentes/")
      .then((res) => res.json())
      .then((data) => setAgentes(data))
      .catch((err) => console.error("Error cargando agentes:", err));
  }, []);
  useEffect(() => {
    fetch("/api/maps/")
      .then((res) => res.json())
      .then((data) => setMaps(data))
      .catch((err) => console.error("Error cargando mapas:", err));
  }, []);

  useEffect(() => {
    if (!selected1) return;
    fetch(`/api/teams/${selected1}/jugadores/`)
      .then((res) => res.json())
      .then((data) => {
        setJugadores1(data);
        console.log("Jugadores cargados1:", data);
        resetAgents("equipo1");
      })
      .catch((err) => console.error("Error cargando jugadores:", err));
  }, [selected1]);

  useEffect(() => {
    if (!selected2) return;
    fetch(`/api/teams/${selected2}/jugadores/`)
      .then((res) => res.json())
      .then((data) => {
        setJugadores2(data);
        console.log("Jugadores cargados2:", data);
        resetAgents("equipo2");
      })
      .catch((err) => console.error("Error cargando jugadores:", err));
  }, [selected2]);

  const handleSelect = (team, target) => {
    if (targetTeam === "equipo1") {
      setSelected1(team.id);
      setIsModalTeam(false);
      console.log("Equipo seleccionado:", team);
      console.log(jugadores1);
    } else if (targetTeam === "equipo2") {
      setSelected2(team.id);
      setIsModalTeam(false);
      console.log("Equipo seleccionado:", team);
    }
    console.log(jugadores2);
  };

 const handleAgentSelect = (agent) => {
  setSelectedAgents((prev) => ({
    ...prev,
    [targetTeam]: agent, 
  }));
  setIsModalAgent(false);
  console.log(`Agente ${agent.nombre} asignado a ${targetTeam}`, agent);
};

  const selectedTeam1 = teams.find((t) => t.id === selected1);
  const selectedTeam2 = teams.find((t) => t.id === selected2);
  const resetAgents = (teamKey) => {
    setSelectedAgents((prev) => {
    const updated = { ...prev };
    Object.keys(updated).forEach((key) => {
      if (key.startsWith(teamKey)) {
        delete updated[key];
      }
    });
    return updated;
  });

};
const mapSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    afterChange: (index) => {
      setCurrentMap(maps[index]); // guardamos el mapa actual
      console.log("Mapa actual:", maps[index]);
    },
  };
  return (
    <div className="app-container">
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
              {jugadores1.map((jugador, index) => (
                <PlayerCard
                  key={`e1-${index}`}
                  jugador={jugador}
                  selectedAgent={selectedAgents[`equipo1-${index}`] || null}
                  onClick={() => {
                    setTargetTeam(`equipo1-${index}`);
                    setIsModalAgent(true);
                  }}
                />
              ))}
            </div>
            </div>
            <div className="map-container">
                <Slider {...mapSettings}>
                    {maps.map((mapa) => (
                        <img
                          src={mapa.imagen_mapa}
                          alt={mapa.nombre}
                          className="map-img"
                        />
                    ))}
                  </Slider>
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
          {jugadores2.map((jugador, index) => (
            <PlayerCard
              key={`e2-${index}`}
              jugador={jugador}
              selectedAgent={selectedAgents[`equipo2-${index}`] || null}
              onClick={() => {
                setTargetTeam(`equipo2-${index}`);
                setIsModalAgent(true);
              }}
            />
          ))}
          </div>
        
          </div>

          {isModalTeam && (
            <div className="modal-overlay">
              <div className="modal">
              <h3 style={{ color: "white", fontFamily: "Verdana, sans-serif" }}>
                Selecciona tu equipo
              </h3>                <div className="team-grid">
                  {teams.map((team) => (
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
                  {agentes.map((agente) => (
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
                  ))}
                </div>
              </div>
            </div>
          )}

        </div>
          <div className="dataContainer"> 
             {currentMap ? currentMap.nombre : "Cargando..."}

            Composición Equipo :
            {jugadores1.map((jugador, index) => {
              const agent = selectedAgents[`equipo1-${index}`];
              return (
                <div key={`comp-e1-${index}`}>
                  {jugador.nombre_jugador}: {agent ? agent.nombre +"  " +agent.rol : "No asignado"}
                </div>
              );
            })}
            Composición Equipo Rival:
            {jugadores2.map((jugador, index) => {
              const agent = selectedAgents[`equipo2-${index}`];
              return (
                <div key={`comp-e2-${index}`}>
                  {jugador.nombre_jugador}: {agent ? agent.nombre +"  " +agent.rol : "No asignado"}
                </div>
              );
            })}
            Probabilidad de victoria Equipo
            Resultado
            Equipo 1 = ataque
            Equipo 2 = defensa
          </div>




          
  </div>
  );
}
