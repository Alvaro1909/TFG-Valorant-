import React from "react";
import "./Player_Card.css";
function PlayerCard({ selectedAgent, jugador, onClick }) {
  return (
    <div className="player-card">
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
