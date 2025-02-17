import { API_URL } from './utils/constants.js';

const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 400;

let leftPaddle, rightPaddle, ball;
let ws;

function initWebSocket() {
  ws = new WebSocket('ws://localhost:8000/ws/game/');

  ws.onopen = () => {
    console.log('Connected to game server');
  };

  ws.onmessage = event => {
    const gameState = JSON.parse(event.data);
    updateGameState(gameState);
  };

  ws.onclose = () => {
    console.log('Disconnected from game server');
    // Reconectar después de un tiempo
    setTimeout(initWebSocket, 1000);
  };
}

function updateGameState(gameState) {
  leftPaddle = gameState.left_paddle;
  rightPaddle = gameState.right_paddle;
  ball = gameState.ball;
  draw();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = 'white';
  ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
  ctx.fillRect(
    rightPaddle.x,
    rightPaddle.y,
    rightPaddle.width,
    rightPaddle.height
  );

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

document.addEventListener('keydown', event => sendKeyEvent(event.key, true));
document.addEventListener('keyup', event => sendKeyEvent(event.key, false));

initWebSocket();
