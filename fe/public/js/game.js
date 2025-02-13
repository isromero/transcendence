// Obtener el canvas y contexto
const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

// Configurar el tamaño del canvas
canvas.width = 800;
canvas.height = 400;

// Definir las palas y la pelota
let leftPaddle = { x: 0, y: canvas.height / 2 - 100 / 2, width: 20, height: 100, color: 'white' };
let rightPaddle = { x: canvas.width - 20, y: canvas.height / 2 - 100 / 2, width: 20, height: 100, color: 'white' };
let ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 20, speedX: 2, speedY: 2, color: 'white' };

// Función para actualizar las palas y la pelota desde el servidor
async function fetchGameState() {
  try {
    const response = await fetch('/game/');
    const data = await response.json();
    leftPaddle = data.left_paddle;
    rightPaddle = data.right_paddle;
    ball = data.ball;
  } catch (error) {
    console.error('Error fetching game state:', error);
  }
}

// Función para dibujar las palas y la pelota
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = leftPaddle.color;
  ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
  ctx.fillStyle = rightPaddle.color;
  ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);
  ctx.fillStyle = ball.color;
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fill();
}

// Llamada al backend cada ciclo del juego
function gameLoop() {
  fetchGameState().then(() => {
    draw();
    requestAnimationFrame(gameLoop);
  });
}

// Iniciar el bucle del juego
gameLoop();
