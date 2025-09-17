import { useEffect, useState } from "react";
import "./App.css";
import TeamSelect from "./componets/Team_Select.js";

export default function App() {
  const [teams, setTeams] = useState([]);
  const [selected1, setSelected1] = useState(null);
  const [jugadores1, setJugadores1] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado para controlar el modal

  useEffect(() => {
    fetch("/api/teams/")
      .then((res) => res.json())
      .then((data) => {
        setTeams(data);
      })
      .catch((err) => {
        console.error("Error cargando equipos:", err);
      });
  fetch("/api/teams/" + selected1 + "/jugadores/")
      .then((res) => res.json())
      .then((data) => {
        setJugadores1(data);
        console.log("Jugadores cargados:", data);
      })
      .catch((err) => {
        console.error("Error cargando jugadores:", err);
      });
  }, [selected1]);

  const handleSelect = (team) => {
    setSelected1(team.id);
    setIsModalOpen(false); 
    console.log("Equipo seleccionado:", team);
    setJugadores1([]);
    console.log(jugadores1);
  };


  const selectedTeam = teams.find((t) => t.id === selected1);

  return (
    <div className="team-container">
      <TeamSelect selectedTeam={selectedTeam} onClick={() => setIsModalOpen(true)} />
    

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Selecciona tu equipo</h3>
            <div className="team-grid">
              {teams.map((team) => (
                <div
                  key={team.id}
                  className="team-card"
                  onClick={() => handleSelect(team)}
                >
                  <img src={team.imagen_equipo} alt={team.nombre} className="team-card img" />
                  <span className="team-name">{team.name}</span>
                </div>
              ))}
            </div>
           
          </div>
        </div>
      )}
    </div>
  );
}