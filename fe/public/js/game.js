import { API_URL } from './utils/constants.js';
import { loadPage } from './router/router.js';

const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 400;

let ws;
let animationFrameId = null;
let gameEnded = false;

function updateGameState(gameState) {


  if (gameState.type === 'init' && gameState.state) {
    gameState = gameState.state; // ⚡ Reemplazarlo con gameState.state
  }
  

  if (gameEnded) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const { left_paddle, right_paddle, ball, scores } = gameState;

  if (!left_paddle || !right_paddle || !ball || !scores) {
    console.error('❌ Estado inválido:', gameState);
    return;
  }

  ctx.fillStyle = '#ff4d6d';
  ctx.fillRect(left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height);
  ctx.fillRect(right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height);

  ctx.fillStyle = 'white';
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fill();

  // 📌 **Si alguien llega a 5 puntos, mostrar el modal y detener el juego**
  if (scores.left >= 5 || scores.right >= 5) {
    console.log('🎉 Fin del juego! Mostrando modal...');

    gameEnded = true;
    stopGame();

    // Usar `loadPage` para abrir el modal correctamente en tu sistema
    console.log('📌 Abriendo modal...');
    loadPage('/modal-end-game');
    console.log('📌 Modal abierto correctamente.');
  } else {
    // Si el juego no ha terminado, seguir animando
    animationFrameId = requestAnimationFrame(() => updateGameState(gameState));
  }
}

// ✅ Asegurar que `stopGame()` detenga el juego completamente
function stopGame() {
  console.log("🛑 Juego detenido");
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  
  if (ws) {
    ws.close();
  }
}

async function checkIfGameFinished(matchId) {
  try {
    const response = await fetch(`${API_URL}/history/match/${matchId}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Error fetching match data');
    }

    if (data.data.status === 'finished') {
      console.log('🎉 Partida ya finalizada, mostrando pantalla de fin de juego...');
      loadPage('/modal-end-game');
      return true; // Indica que el juego ya terminó
    }

    return false; // La partida sigue en curso
  } catch (error) {
    console.error('❌ Error al comprobar el estado del juego:', error);
    return false;
  }
}


// 🎮 **Función de inicialización del juego**
export async function initGame() {
  console.log('Iniciando juego...');

  const path = window.location.pathname;
  const matchId = path.split('/game/')[1];

  if (!matchId) {
    console.log('No se encontró un match_id en la URL');
    return;
  }

  // 🔎 Comprobar si el juego ya terminó antes de abrir WebSocket
  const gameFinished = await checkIfGameFinished(matchId);
  if (gameFinished) return;

  // Iniciar WebSocket si la partida sigue en curso
  ws = new WebSocket(`ws://localhost:8000/ws/game/${matchId}`);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'init_game', match_id: matchId }));
  };

  ws.onmessage = event => {
    const gameState = JSON.parse(event.data);
    updateGameState(gameState);
  };

  ws.onclose = () => {
    console.log('Desconectado del servidor de juego');

    if (!gameEnded) {  // ✅ Solo reiniciar si la partida NO ha terminado
        console.log('♻️ Reconectando en 1 segundo...');
        setTimeout(initGame, 1000);
    } else {
        console.log('🛑 La partida terminó, no se reiniciará el juego.');
    }
};


  window.addEventListener("beforeunload", () => {
    if (ws) {
      ws.send(JSON.stringify({ type: "disconnect" }));
      ws.close();
    }
  });

  document.addEventListener('keydown', event => {
    if (['w', 's', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      sendKeyEvent(event.key, true);
    }
  });

  document.addEventListener('keyup', event => {
    if (['w', 's', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      sendKeyEvent(event.key, false);
    }
  });

  window.addEventListener("popstate", () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("🔙 Navegando atrás, cerrando WebSocket...");
      ws.send(JSON.stringify({ type: "disconnect" }));
      ws.close();
    }
  });
}


// 📡 **Función para enviar eventos de teclado al backend**
function sendKeyEvent(key, isPressed) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'key_event', key, is_pressed: isPressed }));
  }
}

// 📌 **Ejecutar `initGame()` cuando el DOM esté listo**
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('📌 DOM completamente cargado, iniciando juego...');
    initGame();
  });
} else {
  console.log('📌 DOM ya cargado, iniciando juego directamente...');
  initGame();
}