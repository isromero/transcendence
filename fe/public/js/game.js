import { API_URL } from './utils/constants.js';

const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 400;

let ws;

function initGame() {
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
    // Enviar el match_id al servidor
    ws.send(
      JSON.stringify({
        type: 'init_game',
        match_id: matchId,
      })
    );
  };

  // Recibir datos del WebSocket
  ws.onmessage = event => {
    const gameState = JSON.parse(event.data);
    updateGameState(gameState);
  };

  ws.onclose = () => {
    console.log('Desconectado del servidor de juego');
    setTimeout(initGame, 1000); // Reconectar si se desconecta
  };

  // Inicializar las palas y la pelota
  function updateGameState(gameState) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const { left_paddle, right_paddle, ball } = gameState;

    // Dibujar paleta izquierda
    ctx.fillStyle = left_paddle.color || '#ff4d6d'; // Si no hay color, usa uno por defecto
    ctx.fillRect(
      left_paddle.x,
      left_paddle.y,
      left_paddle.width,
      left_paddle.height
    );

    // Dibujar paleta derecha
    ctx.fillStyle = right_paddle.color || '#ff4d6d';
    ctx.fillRect(
      right_paddle.x,
      right_paddle.y,
      right_paddle.width,
      right_paddle.height
    );

    // Dibujar pelota
    ctx.fillStyle = ball.color || 'white';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
  }

  // Enviar el evento de tecla al servidor
  function sendKeyEvent(key, isPressed) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(
        JSON.stringify({
          type: 'key_event',
          key,
          is_pressed: isPressed,
        })
      );
    }
  }

  // Manejar los eventos de teclado
  document.addEventListener('keydown', event => {
    if (['w', 's', 'W', 'S', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      sendKeyEvent(event.key, true);
    }
  });

  document.addEventListener('keyup', event => {
    if (['w', 's', 'W', 'S', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      sendKeyEvent(event.key, false);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initGame();
});
