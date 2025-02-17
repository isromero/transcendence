import { API_URL } from './utils/constants.js';
const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 400;

let leftPaddle, rightPaddle, ball;
let ws;

function initGame() {
  console.log('aaa');
  const canvas = document.getElementById('pong');
  const ctx = canvas.getContext('2d');

  canvas.width = 800;
  canvas.height = 400;

  function initWebSocket() {
    ws = new WebSocket(`ws://localhost:8000/ws/game/`);

    ws.onopen = () => {
      console.log('Conectado al servidor de juego');
    };

    ws.onmessage = event => {
      const gameState = JSON.parse(event.data);
      updateGameState(gameState);
    };

    ws.onclose = () => {
      console.log('Desconectado del servidor de juego');
      setTimeout(initWebSocket, 1000); // Reconectar
    };
  }

  function updateGameState(gameState) {
    // Actualizar estado del juego
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dibujar paletas
    ctx.fillStyle = 'white';
    const { left_paddle, right_paddle, ball } = gameState;

    ctx.fillRect(
      left_paddle.x,
      left_paddle.y,
      left_paddle.width,
      left_paddle.height
    );
    ctx.fillRect(
      right_paddle.x,
      right_paddle.y,
      right_paddle.width,
      right_paddle.height
    );

    // Dibujar pelota
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
  }

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

  // Eventos de teclado
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

  initWebSocket();
}

initGame();
