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
  // console.log('📌 Estado del juego:', gameState);

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
}

// 🎮 **Función de inicialización del juego**
export function initGame() {
  console.log('Iniciando juego...');

  const path = window.location.pathname;
  const matchId = path.split('/game/')[1];

  console.log(matchId);

  if (!matchId) {
    console.log('No se encontró un match_id en la URL');
    return;
  }

  // Iniciar WebSocket
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
    setTimeout(initGame, 1000);
  };

  window.addEventListener("beforeunload", () => {
    if (ws) {
      ws.send(JSON.stringify({ type: "disconnect" }));
      ws.close();
    }
  });

  // 📌 **Eventos de teclado**
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
