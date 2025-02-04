// TODO(ismael) : Remove this for the game??
// Get the canvas and context
const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 400;

// Paddle settings
const paddleWidth = 20;
const paddleHeight = 100;

// Ball settings
const ballSize = 20;

// Left paddle
const leftPaddle = {
  x: 0,
  y: canvas.height / 2 - paddleHeight / 2,
  width: paddleWidth,
  height: paddleHeight,
  color: 'white',
  dy: 0,
};

// Right paddle
const rightPaddle = {
  x: canvas.width - paddleWidth,
  y: canvas.height / 2 - paddleHeight / 2,
  width: paddleWidth,
  height: paddleHeight,
  color: 'white',
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
  ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
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

// Update the position of the ball
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
  }
}

// Move paddles
function movePaddles() {
  // Left paddle
  leftPaddle.y += leftPaddle.dy;
  if (leftPaddle.y <= 0) {
    leftPaddle.y = 0;
  }
  if (leftPaddle.y + leftPaddle.height >= canvas.height) {
    leftPaddle.y = canvas.height - leftPaddle.height;
  }

  // Right paddle
  rightPaddle.y += rightPaddle.dy;
  if (rightPaddle.y <= 0) {
    rightPaddle.y = 0;
  }
  if (rightPaddle.y + rightPaddle.height >= canvas.height) {
    rightPaddle.y = canvas.height - rightPaddle.height;
  }
}

// Control paddles with keyboard
document.addEventListener('keydown', event => {
  if (event.key === 'ArrowUp') {
    rightPaddle.dy = -6;
  } else if (event.key === 'ArrowDown') {
    rightPaddle.dy = 6;
  } else if (event.key === 'w') {
    leftPaddle.dy = -6;
  } else if (event.key === 's') {
    leftPaddle.dy = 6;
  }
});

document.addEventListener('keyup', event => {
  if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
    rightPaddle.dy = 0;
  } else if (event.key === 'w' || event.key === 's') {
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
