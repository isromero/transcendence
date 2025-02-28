document.getElementById("multiplayer-btn").addEventListener("click", () => {
    if (sessionStorage.getItem("matchmaking_active")) {
        alert("❌ Ya estás en el matchmaking.");
        return;
    }

    sessionStorage.setItem("matchmaking_active", "true");

    const ws = new WebSocket("ws://localhost:8000/ws/matchmaking");

    ws.onopen = () => console.log("✅ Buscando partida...");
    
    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "start_match") {
            console.log("✅ Emparejados, creando partida...");
            sessionStorage.removeItem("matchmaking_active"); // ❗ Liberar cuando se inicia la partida
            window.location.href = `/game/${data.match_id}`;
        } else if (data.type === "error") {
            console.error(`❌ Error: ${data.message}`);
            alert(data.message);
            sessionStorage.removeItem("matchmaking_active");
        }
    };

    ws.onclose = () => {
        console.log("🔴 Conexión de matchmaking cerrada");
        sessionStorage.removeItem("matchmaking_active"); // ❗ Liberar al cerrar la conexión
    };

    ws.onerror = (error) => {
        console.error("❌ Error en matchmaking:", error);
        sessionStorage.removeItem("matchmaking_active");
    };
});
