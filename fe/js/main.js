const appContainer = document.getElementById('app-container');
const menuContainer = document.getElementById('menu-container');
const modalBackground = document.getElementById('modal-background');
const modalContainer = document.getElementById('modal-container');

const pageMappings = {
  // Auth pages
  '/auth': '/pages/menus/auth.html',
  '/login': '/pages/menus/login.html',
  '/register': '/pages/menus/register.html',

  // Main pages
  '/': '/pages/menus/auth.html',
  '/home': '/pages/menus/home.html',
  '/create-match': '/pages/menus/create-match.html',
  '/join-match': '/pages/menus/join-match.html',
  '/match-settings': '/pages/menus/match-settings.html',
  '/profile': '/pages/menus/profile.html',
  '/edit-profile': '/pages/menus/edit-profile.html',
  '/social': '/pages/menus/social.html',
  '/friends': '/pages/menus/friends.html',
  '/settings': '/pages/menus/settings.html',

  // Game pages
  '/game': '/pages/game/game.html',

  // Modals
  '/modal-help': '/components/help.html',
  '/modal-languages': '/components/languages.html',
  '/modal-spectate_menu': '/components/spectate_menu.html',
  '/modal-edit_username': '/components/edit-username.html',
  '/modal-edit_mail': '/components/edit-mail.html',
  '/modal-edit_password': '/components/edit-password.html',
  '/modal-verify_email': '/components/verify-email.html',
  '/modal-end_game': '/components/end-game.html',
  '/modal-end_tournament': '/components/end-game-tournament.html',
};

function getCleanPageKey(requestedPath) {
  if (pageMappings[requestedPath]) {
    return requestedPath;
  }

  const filePathKey = Object.keys(pageMappings).find(
    key => pageMappings[key] === requestedPath
  );

  return filePathKey || requestedPath;
}

async function loadPage(page) {
  try {
    closeModal();

    const cleanPage = getCleanPageKey(page);

    const url = pageMappings[cleanPage];
    if (!url) {
      throw new Error(`Page ${cleanPage} not found`);
    }

    if (url.includes('/components/')) {
      await loadModal(url);
    } else if (url.includes('/game/')) {
      await loadGame(url);
    } else {
      await loadMenu(url);
    }

    window.history.pushState({ page: cleanPage }, '', cleanPage);
  } catch (error) {
    console.error('Navigation error:', error);
    loadErrorPage(page, error.message);
  }
}

function closeModal() {
  modalContainer.innerHTML = ''; // Borra el contenido del modal
  modalBackground.hidden = true; // Oculta el fondo oscuro del modal
}

// Cerrar el modal al hacer clic fuera del contenido
modalBackground.addEventListener('click', event => {
  if (event.target === modalBackground) {
    closeModal();
  }
});

// Cerrar el modal al seleccionar un idioma
document.addEventListener('click', event => {
  const languageButton = event.target.closest('.spa-link');
  if (languageButton) {
    closeModal(); // Cierra el modal antes de cambiar la página
  }
});

async function loadMenu(page) {
  try {
    // Use the cleaner URL to get the actual file path
    const url = page; // Fallback to the original page if not found
    const response = await fetch(url);
    const template = await fetch('/pages/templates/menu.html');

    if (!template.ok) {
      throw new Error('Error loading template or page content');
    }
    const template_content = await template.text();
    appContainer.innerHTML = template_content;

    if (!response.ok) {
      throw new Error('Error loading page content');
    }

    const response_content = await response.text();
    const pageContainer = appContainer.querySelector('#page-container');
    if (!pageContainer) {
      throw new Error(
        'Element with ID "page-container" not found in the template'
      );
    }
    pageContainer.innerHTML = response_content;

    updateIcons(page);
  } catch (error) {
    loadErrorPage(page, error.message);
  }
}

async function loadGame(page) {
  try {
    const url = page;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }
    const response_content = await response.text();
    appContainer.innerHTML = response_content;
    setTimeout(() => {
      // TODO(ismael) : Remove this for the game??
      //startGame();
    }, 0);
  } catch (error) {
    loadErrorPage(page, error.message);
  }
}

async function loadModal(page) {
  try {
    const url = page;
    const response = await fetch(url);

    modalBackground.hidden = false;

    if (!response.ok) {
      throw new Error('Error loading template or page content');
    }

    const response_content = await response.text();
    modalContainer.innerHTML = response_content;
  } catch (error) {
    loadErrorPage(page, error.message);
  }
}

function loadErrorPage(requestedPage, message) {
  try {
    const errorContent = `
      <div class="text-center p-5">
        <h2>Error loading page: ${requestedPage}</h2>
        <p>${message}</p>
        <a href="/" class="spa-link btn btn-primary">Return to Home</a>
      </div>`;

    appContainer.innerHTML = errorContent;
    window.history.replaceState({ page: '/' }, '', '/');
  } catch (error) {
    console.error('Critical error handling failed:', error);
    appContainer.innerHTML =
      '<h1 class="text-center p-5">Critical error occurred</h1>';
  }
}

function updateIcons(page) {
  const leftButton = document.querySelector(
    '.btn.position-absolute.bottom-0.start-0 i'
  );
  const rightButton = document.querySelector(
    '.btn.position-absolute.bottom-0.end-0 i'
  );

  if (!leftButton || !rightButton) {
    console.warn('Navigation buttons not found in the DOM');
    return;
  }

  // Extract the page type from the URL
  const isMenuPage = page.includes('/pages/menus/');
  const isGamePage = page.includes('/pages/game/');
  const pageType = page.split('/').pop().replace('.html', '');

  // Set default attributes
  leftButton.className = 'bi bi-person-circle';
  leftButton.parentElement.setAttribute('href', '/profile');
  rightButton.className = 'bi bi-list';
  rightButton.parentElement.setAttribute('href', '/settings');

  // Special cases for authentication pages
  if (pageType === 'auth' || pageType === 'login' || pageType === 'register') {
    leftButton.className = 'bi bi-question-circle';
    leftButton.parentElement.setAttribute('href', '/modal-help');
    rightButton.className = 'bi bi-globe';
    rightButton.parentElement.setAttribute('href', '/modal-languages');
  }

  // Special cases for game pages
  if (isGamePage) {
    leftButton.className = 'bi bi-arrow-left';
    leftButton.parentElement.setAttribute('href', '/auth');
    rightButton.className = 'bi bi-pause';
    rightButton.parentElement.setAttribute('href', '/modal-pause');
  }
}

document.body.addEventListener('click', event => {
  const link = event.target.closest('a.spa-link');

  if (link) {
    event.preventDefault();
    const page = link.getAttribute('href');
    loadPage(page);
  }
});

window.addEventListener('popstate', event => {
  const rawPage = event.state?.page || window.location.pathname;
  const page = getCleanPageKey(rawPage);
  loadPage(page);
});

loadPage(window.location.pathname);

// TODO(ismael) : Remove this for the game??
/* function startGame() {
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
    x: canvas.width - paddleWidth - 30,
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
 */
