import { loadPage } from '../router/router.js';

document.getElementById("multiplayer-btn").addEventListener("click", () => {
    const ws = new WebSocket("ws://localhost:8000/ws/matchmaking");

    ws.onopen = () => console.log("✅ Buscando partida...");
    
    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "start_match") {
            console.log("✅ Emparejados, match ID recibido:", data.match_id);

            // ✅ No es necesario volver a crear la partida en el backend
            let matchId = data.match_id;

            // Redirigir directamente al juego con el matchId
            window.location.href = `/game/${matchId}`;
        } else if (data.type === "error") {
            console.error(`❌ Error: ${data.message}`);
            alert(data.message);
        }
    };

    ws.onerror = (error) => console.error("❌ Error en matchmaking:", error);
    ws.onclose = () => console.log("🔴 Conexión de matchmaking cerrada");
});
