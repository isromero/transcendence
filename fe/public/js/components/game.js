import { parseAndSetContent } from '../utils/helpers.js';

const appContainer = document.getElementById('app-container');

export async function loadGame(page) {
  try {
    const response = await fetch(page);

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const responseContent = await response.text();
    appContainer.innerHTML = responseContent;

    setTimeout(() => {
      startGame(); // TODO: LLAMAR A INIT GAME
    }, 0);

    parseAndSetContent(appContainer, responseContent);
  } catch (error) {
    console.error('Error loading game:', error.message);
  }
}

// TODO: DELETE THIS FUNCTION. TIENE TODA LA LÓGICA EN EL FRONT, Y HABRÍA QUE COGER LOS DATOS DEL WEBSOCKET
function startGame() {
  const canvas = document.getElementById('pong');
  if (!canvas) {
    console.error('Canvas element not found!');
    return;
  }
  const ctx = canvas.getContext('2d');

  canvas.width = 800;
  canvas.height = 400;

  const paddleWidth = 20;
  const paddleHeight = 100;
  const ballSize = 20;

  const leftPaddle = {
    x: 30,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: '#ff4d6d',
    dy: 0,
  };

  const rightPaddle = {
    x: canvas.width - paddleWidth - 30,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: '#ff4d6d',
    dy: 0,
  };

  const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: ballSize,
    speedX: 4, // Aumentamos la velocidad a 4
    speedY: 4, // Aumentamos la velocidad a 4
    color: 'white',
  };

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = leftPaddle.color;
    ctx.fillRect(
      leftPaddle.x,
      leftPaddle.y,
      leftPaddle.width,
      leftPaddle.height
    );

    ctx.fillStyle = rightPaddle.color;
    ctx.fillRect(
      rightPaddle.x,
      rightPaddle.y,
      rightPaddle.width,
      rightPaddle.height
    );

    ctx.fillStyle = ball.color;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
  }

  function updateBall() {
    ball.x += ball.speedX;
    ball.y += ball.speedY;

    if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
      ball.speedY = -ball.speedY;
    }

    function checkPaddleCollision(paddle) {
      if (
        ball.x - ball.radius <= paddle.x + paddle.width &&
        ball.x + ball.radius >= paddle.x &&
        ball.y >= paddle.y &&
        ball.y <= paddle.y + paddle.height
      ) {
        const relativeIntersectY =
          (ball.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2);
        const bounceAngle = (relativeIntersectY * Math.PI) / 4;

        const speed = Math.sqrt(ball.speedX ** 2 + ball.speedY ** 2);
        ball.speedX =
          (paddle === leftPaddle ? 1 : -1) *
          Math.cos(bounceAngle) *
          speed *
          1.1;
        ball.speedY = Math.sin(bounceAngle) * speed * 1.1;
      }
    }

    checkPaddleCollision(leftPaddle);
    checkPaddleCollision(rightPaddle);

    if (ball.x - ball.radius <= 0 || ball.x + ball.radius >= canvas.width) {
      ball.x = canvas.width / 2;
      ball.y = canvas.height / 2;
      ball.speedX = 4 * (Math.random() > 0.5 ? 1 : -1); // Mantener la velocidad más alta
      ball.speedY = 4 * (Math.random() > 0.5 ? 1 : -1); // Mantener la velocidad más alta
    }
  }

  const paddleSpeed = 4; // La velocidad de las paletas se mantiene igual

  function movePaddles() {
    leftPaddle.y += leftPaddle.dy;
    rightPaddle.y += rightPaddle.dy;

    // Limitar las paletas dentro del área del campo
    leftPaddle.y = Math.max(
      0,
      Math.min(canvas.height - leftPaddle.height, leftPaddle.y)
    );
    rightPaddle.y = Math.max(
      0,
      Math.min(canvas.height - rightPaddle.height, rightPaddle.y)
    );
  }

  // Manejador de eventos de las teclas presionadas (keydown)
  document.addEventListener('keydown', event => {
    // Mueve la paleta derecha
    if (event.key === 'ArrowUp') {
      rightPaddle.dy = -paddleSpeed;
    }
    if (event.key === 'ArrowDown') {
      rightPaddle.dy = paddleSpeed;
    }

    // Mueve la paleta izquierda
    if (event.key === 'w' || event.key === 'W') {
      leftPaddle.dy = -paddleSpeed;
    }
    if (event.key === 's' || event.key === 'S') {
      leftPaddle.dy = paddleSpeed;
    }
  });

  // Manejador de eventos de las teclas soltadas (keyup)
  document.addEventListener('keyup', event => {
    // Detener el movimiento de la paleta derecha
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      rightPaddle.dy = 0;
    }

    // Detener el movimiento de la paleta izquierda
    if (
      event.key === 'w' ||
      event.key === 's' ||
      event.key === 'W' ||
      event.key === 'S'
    ) {
      leftPaddle.dy = 0;
    }
  });

  function gameLoop() {
    draw();
    movePaddles();
    updateBall();
    requestAnimationFrame(gameLoop);
  }

  gameLoop();
}
