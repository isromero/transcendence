// Verificar si el jugador está en cola al cargar la página o al navegar atrás
window.addEventListener("load", () => {
    if (sessionStorage.getItem("matchmaking_active")) {
      // Si hay un matchmaking activo, mostramos la cola
      document.getElementById("queue-status").style.display = "block";
      document.getElementById("local-match-btn").style.display = "none";
      document.getElementById("multiplayer-btn").style.display = "none";
    } else {
      // Si no está en cola, restauramos los botones de selección de partida
      document.getElementById("local-match-btn").style.display = "block";
      document.getElementById("multiplayer-btn").style.display = "block";
      document.getElementById("queue-status").style.display = "none";
    }
  });
  
  // Manejo del clic en "Multiplayer" para unirse al matchmaking
  document.getElementById("multiplayer-btn").addEventListener("click", () => {
    // Si ya está en el matchmaking, no hacer nada
    if (sessionStorage.getItem("matchmaking_active")) {
      alert("❌ Ya estás en el matchmaking.");
      return;
    }
  
    // Mostrar el estado de cola
    document.getElementById("queue-status").style.display = "block";
  
    // Ocultar los botones de selección de partida
    document.getElementById("local-match-btn").style.display = "none";
    document.getElementById("multiplayer-btn").style.display = "none";
  
    // Establecer el estado en matchmaking
    sessionStorage.setItem("matchmaking_active", "true");
  
    // Crear una nueva conexión WebSocket
    const ws = new WebSocket("ws://localhost:8000/ws/matchmaking");
  
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
  
    // Agregar funcionalidad para el botón de cancelar cola
    document.getElementById("cancel-queue-btn").addEventListener("click", () => {
      ws.close();  // Cerrar la conexión WebSocket
      sessionStorage.removeItem("matchmaking_active");
  
      // Restaurar la UI
      document.getElementById("queue-status").style.display = "none";
      document.getElementById("local-match-btn").style.display = "block";
      document.getElementById("multiplayer-btn").style.display = "block";
    });
  });
  
  // Detectar cuando el usuario navega hacia atrás (con "popstate")
  window.addEventListener("popstate", () => {
    // Si el estado de matchmaking está activo, pero la cola no está visible, se debe cancelar
    if (sessionStorage.getItem("matchmaking_active") && document.getElementById("queue-status").style.display !== "block") {
      // Cancelar el estado de cola y restaurar la UI
      sessionStorage.removeItem("matchmaking_active");
  
      document.getElementById("queue-status").style.display = "none";
      document.getElementById("local-match-btn").style.display = "block";
      document.getElementById("multiplayer-btn").style.display = "block";
    }
  });
  
  // Detectar cuando el usuario refresca la página o sale (beforeunload)
  window.addEventListener("beforeunload", () => {
    // Si el jugador estaba en cola y se cierra la página, eliminamos el estado
    if (sessionStorage.getItem("matchmaking_active")) {
      sessionStorage.removeItem("matchmaking_active");
    }
  });
  