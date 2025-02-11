const appContainer = document.getElementById('app-container');

export async function loadGame(page) {
  try {
    const url = page;
    const response = await fetch(url);

    console.log(page);

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }
    const response_content = await response.text();
    appContainer.innerHTML = response_content;
    setTimeout(() => {
      startGame();
    }, 0);
  } catch (error) {
    loadError('?', error.message);
  }
}

function startGame() {
  const canvas = document.getElementById('pong');
  if (!canvas) {
    console.error('Canvas element not found!');
    return;
  }
  const ctx = canvas.getContext('2d');
  // Set canvas size
  canvas.width = 800;
  canvas.height = 400;
  // Paddle settings
  const paddleWidth = 20;
  const paddleHeight = 100;
  const paddleMovement = 1;
  // Ball settings
  const ballSize = 20;
  // Left paddle
  const leftPaddle = {
    x: 30,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: '#ff4d6d',
    dy: 0,
  };
  // Right paddle
  const rightPaddle = {
    x: (canvas.width - paddleWidth) - 30,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: '#ff4d6d',
    dy: 0,
  };
  // Ball
  const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: ballSize,
    speedX: 2,
    speedY: 2,
    color: 'white',
  };
  // Draw paddles and ball
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw paddles
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
    // Draw ball
    ctx.fillStyle = ball.color;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
  }
  // Update ball position
  function updateBall() {
    ball.x += ball.speedX;
    ball.y += ball.speedY;
    // Ball collision with top and bottom
    if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
      ball.speedY = -ball.speedY;
    }
    // Ball collision with paddles
    if (
      ball.x - ball.radius <= leftPaddle.x + leftPaddle.width &&
      ball.y >= leftPaddle.y &&
      ball.y <= leftPaddle.y + leftPaddle.height
    ) {
      ball.speedX = -ball.speedX * 1.1;
    }
    if (
      ball.x + ball.radius >= rightPaddle.x &&
      ball.y >= rightPaddle.y &&
      ball.y <= rightPaddle.y + rightPaddle.height
    ) {
      ball.speedX = -ball.speedX * 1.1;
    }
    // Ball out of bounds
    if (ball.x - ball.radius <= 0 || ball.x + ball.radius >= canvas.width) {
      ball.x = canvas.width / 2;
      ball.y = canvas.height / 2;
      ball.speedX = 1.5;
      ball.speedY = 1.5;
    }
  }
  // Move paddles
  function movePaddles() {
    leftPaddle.y += leftPaddle.dy;
    rightPaddle.y += rightPaddle.dy;
    // Paddle collision with walls
    leftPaddle.y = Math.max(
      0,
      Math.min(canvas.height - leftPaddle.height, leftPaddle.y)
    );
    rightPaddle.y = Math.max(
      0,
      Math.min(canvas.height - rightPaddle.height, rightPaddle.y)
    );
  }
  // Keyboard controls
  document.addEventListener('keydown', event => {
    if (event.key === 'ArrowUp') {
      rightPaddle.dy = -paddleMovement;
    } else if (event.key === 'ArrowDown') {
      rightPaddle.dy = paddleMovement;
    } else if (event.key === 'w') {
      leftPaddle.dy = -paddleMovement;
    } else if (event.key === 's') {
      leftPaddle.dy = paddleMovement;
    }
  });
  document.addEventListener('keyup', event => {
    if (['ArrowUp', 'ArrowDown'].includes(event.key)) {
      rightPaddle.dy = 0;
    }
    if (['w', 's'].includes(event.key)) {
      leftPaddle.dy = 0;
    }
  });
  // Game loop
  function gameLoop() {
    draw();
    movePaddles();
    updateBall();
    requestAnimationFrame(gameLoop);
  }
  gameLoop();
}
