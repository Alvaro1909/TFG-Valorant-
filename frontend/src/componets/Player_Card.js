import React from "react";


function PlayerCard({ selectedTeam, player,selectedAgent}) {
  return (
    <div className="player-card">
      <img src={player.imagen_jugador} alt={player.nombre_jugador} className="player-image" />
      <h4 className="player-name">{player.nombre_jugador}</h4>
      <p className="player-role">{player.rol}</p>
    </div>
  );
}