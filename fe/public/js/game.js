const canvas = document.getElementById("pong");
const ctx = canvas.getContext("2d");

canvas.width = 800;
canvas.height = 400;

let leftPaddle, rightPaddle, ball;

async function fetchGameState() {
  try {
    const response = await fetch("/game/");
    const data = await response.json();
    leftPaddle = data.left_paddle;
    rightPaddle = data.right_paddle;
    ball = data.ball;
  } catch (error) {
    console.error("Error fetching game state:", error);
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "white";
  ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
  ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);

  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fill();
}

function gameLoop() {
  fetchGameState().then(draw);
  requestAnimationFrame(gameLoop);
}

document.addEventListener("keydown", (event) => sendKeyEvent(event.key, true));
document.addEventListener("keyup", (event) => sendKeyEvent(event.key, false));

async function sendKeyEvent(key, isPressed) {
  try {
    await fetch("/game/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, is_pressed: isPressed }),
    });
  } catch (error) {
    console.error("Error sending key event:", error);
  }
}

gameLoop();
