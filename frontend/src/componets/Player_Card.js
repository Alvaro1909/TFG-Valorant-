import React from "react";
import "./Player_Card.css";
function PlayerCard({ selectedAgent, jugador, onClick, highlight }) {
  const getBackgroundColor = () => {
    if (highlight === "high") return "#28a745";
    if (highlight === "low") return "#d9534f";
    return "#a2a2a2"; 
  };

  return (
    <div className="player-card" style={{ backgroundColor: getBackgroundColor() }}>
    <button
      className="agent-select-button"
      onClick={onClick}
      title={selectedAgent ? selectedAgent.name : "Seleccionar agente"}
    >
      {selectedAgent ? (
        <img
          src={selectedAgent.imagen_personaje}
          alt={selectedAgent.nombre}
          className="agent-select-img"
        />
      ) : (
        <span className="agent-select-placeholder">+</span>
      )}
    </button>
    <span className="player-name">{jugador.nombre_jugador}</span>
    </div>
  );
}

export default PlayerCard;
