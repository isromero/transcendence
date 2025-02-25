import { API_URL } from './utils/constants.js';

const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 400;

let ws;

// 🔄 **Función global para actualizar el estado del juego**
function updateGameState(gameState) {
  console.log('📌 Recibiendo estado del juego:', gameState);
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const { left_paddle, right_paddle, ball } = gameState;

  if (!left_paddle || !right_paddle || !ball) {
    console.error('❌ Estado del juego inválido:', gameState);
    return;
  }

  // Dibujar paleta izquierda
  ctx.fillStyle = left_paddle.color || '#ff4d6d';
  ctx.fillRect(left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height);

  // Dibujar paleta derecha
  ctx.fillStyle = right_paddle.color || '#ff4d6d';
  ctx.fillRect(right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height);

  // Dibujar pelota
  ctx.fillStyle = ball.color || 'white';
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fill();
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
    console.log('Conectado al servidor de juego');
    ws.send(JSON.stringify({ type: 'init_game', match_id: matchId }));
  };

  ws.onmessage = event => {
    console.log('📡 Mensaje recibido del servidor');
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

  window.addEventListener("beforeunload", () => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "disconnect" }));  // Notifica al servidor
        socket.close();  // Cierra el socket
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

// 🔄 Hacer que initGame sea accesible desde la consola
window.initGame = initGame;
