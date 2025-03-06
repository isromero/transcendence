let ws = null; // Mantener la referencia global al WebSocket

document.getElementById("multiplayer-btn").addEventListener("click", () => {
    // Si ya está en el matchmaking, no hacer nada
    if (sessionStorage.getItem("matchmaking_active")) {
        alert("❌ Ya estás en el matchmaking.");
        return;
    }

    // Asegurarse de que no haya un WebSocket viejo
    if (ws) {
        ws.close();
        ws = null;
    }

    // Mostrar el estado de cola
    document.getElementById("queue-status").style.display = "block";

    // Ocultar los botones de selección de partida
    document.getElementById("local-match-btn").style.display = "none";
    document.getElementById("multiplayer-btn").style.display = "none";

    // Establecer el estado en matchmaking
    sessionStorage.setItem("matchmaking_active", "true");

    // Crear una nueva conexión WebSocket
    ws = new WebSocket("ws://localhost:8000/ws/matchmaking");

    ws.onopen = () => console.log("✅ Buscando partida...");

    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        console.log("📩 [WebSocket] Mensaje recibido:", data);

        if (data.type === "start_match") {
            console.log("✅ Emparejados, creando partida...");
            console.log("🎮 Rol recibido desde el servidor:", data.player);

            sessionStorage.removeItem("matchmaking_active");
            sessionStorage.setItem("player_role", data.player);

            window.location.href = `/game/${data.match_id}`;
        } else if (data.type === "error") {
            console.error(`❌ Error: ${data.message}`);
            alert(data.message);
            sessionStorage.removeItem("matchmaking_active");

            // Restaurar la UI si hay un error
            document.getElementById("queue-status").style.display = "none";
            document.getElementById("local-match-btn").style.display = "block";
            document.getElementById("multiplayer-btn").style.display = "block";
        }
    };

    ws.onclose = () => {
        console.log("🔴 Conexión de matchmaking cerrada");
        sessionStorage.removeItem("matchmaking_active");

        // Restaurar la UI cuando la conexión se cierre
        document.getElementById("queue-status").style.display = "none";
        document.getElementById("local-match-btn").style.display = "block";
        document.getElementById("multiplayer-btn").style.display = "block";
    };

    ws.onerror = (error) => {
        console.error("❌ Error en matchmaking:", error);
        sessionStorage.removeItem("matchmaking_active");

        // Restaurar la UI en caso de error
        document.getElementById("queue-status").style.display = "none";
        document.getElementById("local-match-btn").style.display = "block";
        document.getElementById("multiplayer-btn").style.display = "block";
    };

    //TODO: ADRI E ISMA MIRAR LOGICA DE POPSATE
    // Manejo del botón de cancelar cola
    document.getElementById("cancel-queue-btn").addEventListener("click", () => {
        if (ws) {
            ws.close();
            ws = null;
        }
        sessionStorage.removeItem("matchmaking_active");

        // Restaurar la UI
        document.getElementById("queue-status").style.display = "none";
        document.getElementById("local-match-btn").style.display = "block";
        document.getElementById("multiplayer-btn").style.display = "block";
    });
});

// TODO:IMSAA LEEE AQUIII!!! FIJATE QUE LA LOGICA DE ENCIMA DE CANCEL BTN Y LA DE DEBAJO DE POPSTATE SON LA MISMA
// Manejo del botón "atrás" del navegador (popstate)
window.addEventListener("popstate", () => {

    console.log("🔙 Usuario navegó hacia atrás");
    document.getElementById("multiplayer-btn").removeEventListener("click", () => {});

    // Si el matchmaking está activo, replicamos la acción de cancelar cola
    if (sessionStorage.getItem("matchmaking_active")) {
        // Cerrar el WebSocket
        if (ws) {
            ws.close();
            ws = null;
        }

        // Eliminar el estado de matchmaking
        sessionStorage.removeItem("matchmaking_active");

        // Restaurar la UI al estado inicial
        document.getElementById("queue-status").style.display = "none";
        document.getElementById("local-match-btn").style.display = "block";
        document.getElementById("multiplayer-btn").style.display = "block";
    }
});

// Detectar cuando el usuario refresca la página o sale
window.addEventListener("beforeunload", () => {
    if (sessionStorage.getItem("matchmaking_active")) {
        sessionStorage.removeItem("matchmaking_active");
        if (ws) {
            ws.close();
            ws = null;
        }
    }
});
