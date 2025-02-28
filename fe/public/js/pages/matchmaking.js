import { loadPage } from '../router/router.js';


document.getElementById("multiplayer-btn").addEventListener("click", () => {
    const ws = new WebSocket("ws://localhost:8000/ws/matchmaking");

    ws.onopen = () => console.log("✅ Buscando partida...");
    
    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "start_match") {
            console.log("✅ Emparejados, creando partida...");

            // Llamar a createMatch.js para generar la partida
            await createMatch();
        }
    };

    ws.onerror = (error) => console.error("❌ Error en matchmaking:", error);
    ws.onclose = () => console.log("🔴 Conexión de matchmaking cerrada");
});

async function createMatch() {
    try {
        const response = await fetch('http://localhost:8000/api/history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ local_match: true }), // Indicar que es multijugador
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to create match.');
        }

        const matchId = data.data.match_id;
        console.log(`✅ Match ID recibido: ${matchId}`);

        if (!matchId) {
            throw new Error('❌ Match ID no válido o vacío.');
        }

        // Redirigir a la página del juego
        window.history.pushState({}, '', `/game/${matchId}`);
        loadPage(`/game/${matchId}`);
    } catch (error) {
        console.error('❌ Error creando partida:', error);
        alert('Error creating match. Please try again.');
    }
}
