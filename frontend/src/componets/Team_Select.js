import React from "react";
import "./Team_Select.css";

function TeamSelect({ selectedTeam, onClick }) {
  return (
    <button className="team-select-button" onClick={onClick} title={selectedTeam?.name || "Seleccionar equipo"}>
      {selectedTeam ? (
        <img src={selectedTeam.imagen_equipo} alt={selectedTeam.nombre_equipo} className="team-select-img" />
      ) : (
        <span className="team-select-placeholder">+</span>
      )}
    </button>
  );
}

export default TeamSelect;