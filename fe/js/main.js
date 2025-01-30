const appContainer = document.getElementById('app-container');
const menuContainer = document.getElementById('menu-container');
const modalBackground = document.getElementById('modalus-background');
const modalContainer = document.querySelector('#modal-container');

async function loadPage(page) {
  if (!page) return;

  // Cierra cualquier modal abierto ANTES de cambiar la página
  closeModal();

  let url;

  if (page === '/' || page == '/index.html') {
    page = '/menu-auth';
  }

  if (page.includes('menu-')) {
    page = page.replace('/menu-', '');
    url = `/pages/menus/${page}.html`;
    loadMenu(url);
  } else if (page.includes('game-')) {
    page = page.replace('/game-', '');
    url = `/pages/game/${page}.html`;
    loadGame(url);
  } else if (page.includes('modal-')) {
    page = page.replace('/modal-', '');
    url = `/components/${page}.html`;
    loadModal(url);
  } else {
    const message = `not found page: ${page}`;
    loadError(404, message);
  }
}

function closeModal() {
  modalContainer.innerHTML = ""; // Borra el contenido del modal
  modalBackground.hidden = true; // Oculta el fondo oscuro del modal
}


async function loadMenu(page) {
  try {
    const url = page;
    const response = await fetch(url);
    const template = await fetch('/pages/templates/menu.html');

    if (!template.ok) {
      throw new Error('Error loading template or page content');
    }
    const template_content = await template.text();
    appContainer.innerHTML = template_content;
    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const response_content = await response.text();
    const pageContainer = appContainer.querySelector('#page-container');
    if (!pageContainer) {
      throw new Error(
        'Element with ID "page-container" not found in the template'
      );
    }
    pageContainer.innerHTML = response_content;
    //updateIcons(page);
  } catch (error) {
    loadError('?', error.message);
  }
}

async function loadGame(page) {
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

async function loadModal(page) {
  try {
    const url = page;
    console.log(url);
    const response = await fetch(url);

    modalBackground.hidden = false;

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const response_content = await response.text();
    modalContainer.innerHTML = response_content;
  } catch (error) {
    loadError('willyyyyyy', error.message);
  }
}

async function loadError(page, message) {
  try {
    const url = page;
    const response = await fetch(url);

    if (!response.ok) {
      /* TODO(samusanc): here goes an error checker for debug and other stuff, throw
       * exception is a mistake!!!*/
      throw new Error('Error page not found');
    }

    const content = await response.text();
    pageContainer.innerHTML = content;

    //window.history.pushState({ page }, '', page);
    //updateIcons(page);
  } catch (error) {
    loadError('ay que se quema la casa', error.message);
  }
}

document.body.addEventListener('click', event => {
  const link = event.target.closest('a.spa-link');

  if (link) {
    event.preventDefault();
    const page = link.getAttribute('href');
    console.log(page);
    loadPage(page);
  }
});

window.addEventListener('popstate', event => {
  console.log('test');
  const page = event.state?.page || '/';
  loadPage(page);
});

loadPage(window.location.pathname);

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
