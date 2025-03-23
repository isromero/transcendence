import { loadPage } from './router/router.js';
import { showErrorToast, updateTournamentUI } from './utils/helpers.js';
import { historyService } from './services/history.js';
import { IMAGES_URL } from './utils/constants.js';
let canvas;
let ctx;
let ws;
let animationFrameId = null;
let gameEnded = false;
let isInitializing = false;
let hasNavigatedAway = false;

function resetGameState() {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }

  if (ws && ws.readyState === WebSocket.OPEN) {
    try {
      ws.send(JSON.stringify({ type: 'disconnect' }));
      ws.close();
    } catch (error) {
      console.error('Error closing WebSocket:', error);
    }
  }

  gameEnded = false;
  ws = null;
  canvas = null;
  ctx = null;
  isInitializing = false;
  hasNavigatedAway = false;
}

async function updateGameState(gameState) {
  try {
    if (gameState.type === 'init' && gameState.state) {
      gameState = gameState.state;
    }

    if (gameEnded) {
      return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const { left_paddle, right_paddle, ball, scores, countdown } = gameState;

    if (!left_paddle || !right_paddle || !ball || !scores) {
      console.error('Invalid game state:', gameState);
      return;
    }

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = 'white';
    ctx.font = '40px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${scores.left} - ${scores.right}`, canvas.width / 2, 50);
    if (countdown && countdown > 0) {
      ctx.fillStyle = 'white';
      ctx.font = '80px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(Math.ceil(countdown), canvas.width / 2, canvas.height / 2);
    }

    ctx.fillStyle = '#ff4d6d';
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

    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();

    // If someone reaches 5 points, show the modal and stop the game
    if (scores.left >= 5 || scores.right >= 5) {
      gameEnded = true;
      stopGame();

      const path = window.location.pathname;
      // If the game is in a tournament, redirect to the tournament page
      if (path.includes('/tournament/')) {
        const joinCode = path.split('/tournament/')[1]?.split('/')[0];
        await loadPage(`/tournament/${joinCode}`);
        // TODO: THIS IS NOT WORKING WELL
        updateTournamentUI(joinCode);
      } else {
        // If it's a multiplayer or local game, show the modal
        await loadPage('/modal-end-game');

        const matchId = path.split('/game/')[1]?.split('/')[0];
        const data = await historyService.getMatchHistory(matchId);

        setWinner(data);
      }
    } else {
      // If the game is not ended, continue animating
      animationFrameId = requestAnimationFrame(() =>
        updateGameState(gameState)
      );
    }
  } catch (error) {
    console.error('Error in updateGameState:', error);
  }
}

function stopGame() {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }

  if (ws) {
    try {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'disconnect' }));
      }
      ws.close();
    } catch (error) {
      console.error('Error closing WebSocket in stopGame:', error);
    }
  }
}

const setWinner = data => {
  const winnerImage = document.getElementById('winner-image');
  const winnerUsername = document.getElementById('winner-username');

  if (!winnerImage || !data?.players) {
    return;
  }

  const isLocalMatch = data.is_local;
  const winner = data.players.find(player => player.is_winner);

  if (winner) {
    winnerImage.src = winner.avatar
      ? `${IMAGES_URL}${winner.avatar.replace('/images/', '/')}`
      : `${IMAGES_URL}/default_avatar.webp`;

    if (isLocalMatch) {
      winnerUsername.textContent = winner.is_player1 ? 'Player 1' : 'Player 2';
    } else {
      winnerUsername.textContent = winner.username || 'Unknown Player';
    }
  }
};

async function checkIfGameFinished(matchId) {
  try {
    const data = await historyService.getMatchHistory(matchId);

    if (data && data.status === 'finished') {
      await loadPage('/modal-end-game');
      setWinner(data);
      return true;
    }

    return false;
  } catch (error) {
    console.error('Error checking game status:', error);
    return false;
  }
}

async function startCountdown() {
  const countdownElement = document.getElementById('countdown');
  let count = 5;

  return new Promise(resolve => {
    const interval = setInterval(() => {
      console.log('Countdown:', count); // Debugging

      countdownElement.textContent = count;
      count--;

      if (count < 0) {
        clearInterval(interval);
        countdownElement.style.display = 'none'; // Ocultar el contador
        resolve();
      }
    }, 1000);
  });
}

export async function initGame() {
  // Prevent multiple simultaneous initializations
  if (isInitializing) {
    return;
  }

  isInitializing = true;
  await startCountdown();

  try {
    resetGameState();

    try {
      canvas = document.getElementById('pong');
      ctx = canvas.getContext('2d');
      canvas.width = 800;
      canvas.height = 400;
    } catch (error) {
      console.error('Error waiting for canvas:', error);
      isInitializing = false;
      return;
    }

    const path = window.location.pathname;
    const matchId = path.split('/game/')[1]?.split('/')[0];

    if (!matchId) {
      console.error('No valid match ID found');
      isInitializing = false;
      return;
    }

    // Check if the game already finished before opening WebSocket
    const gameFinished = await checkIfGameFinished(matchId);
    if (gameFinished) {
      isInitializing = false;
      return;
    }

    // Start WebSocket if the game is still ongoing
    try {
      ws = new WebSocket(`ws://localhost:8000/ws/game/${matchId}`);

      ws.onopen = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'init_game', match_id: matchId }));
        }
      };

      ws.onmessage = event => {
        try {
          const gameState = JSON.parse(event.data);
          updateGameState(gameState);
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        if (!gameEnded && !hasNavigatedAway) {
          // If the game is not ended and the user has not navigated away,
          // wait 1 second and try to initialize the game again
          setTimeout(initGame, 1000);
        }
      };

      ws.onerror = error => {
        showErrorToast(`Error connecting to the game: ${error}`);
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      isInitializing = false;
      return;
    }

    // Eliminate previous listeners to avoid duplicates
    document.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('keyup', handleKeyUp);

    // Add new listeners
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);

    // When the user closes the tab, the game is closed
    window.removeEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('beforeunload', handleBeforeUnload);

    // When the user goes back to the previous page, the game is closed
    window.removeEventListener('popstate', handlePopState);
    window.addEventListener('popstate', handlePopState);
  } catch (error) {
    console.error('Error in general in initGame:', error);
  } finally {
    isInitializing = false;
  }
}

function handleKeyDown(event) {
  try {
    const playerRole = sessionStorage.getItem('player_role');
    const isLocalMatch = true;

    if (
      isLocalMatch ||
      (playerRole === 'left' && ['w', 's'].includes(event.key)) ||
      (playerRole === 'right' && ['ArrowUp', 'ArrowDown'].includes(event.key))
    ) {
      sendKeyEvent(event.key, true);
    }
  } catch (error) {
    console.error('Error in handleKeyDown:', error);
  }
}

function handleKeyUp(event) {
  try {
    const playerRole = sessionStorage.getItem('player_role');
    const isLocalMatch = true;

    if (
      isLocalMatch ||
      (playerRole === 'left' && ['w', 's'].includes(event.key)) ||
      (playerRole === 'right' && ['ArrowUp', 'ArrowDown'].includes(event.key))
    ) {
      sendKeyEvent(event.key, false);
    }
  } catch (error) {
    console.error('Error in handleKeyUp:', error);
  }
}

function handleBeforeUnload() {
  try {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'disconnect' }));
      ws.close();
      stopGame();
    }
  } catch (error) {
    console.error('Error in handleBeforeUnload:', error);
  }
}

// Function to clean all game resources when navigating away from the page
function cleanupGameResources() {
  stopGame();

  document.removeEventListener('keydown', handleKeyDown);
  document.removeEventListener('keyup', handleKeyUp);
  window.removeEventListener('beforeunload', handleBeforeUnload);
  window.removeEventListener('popstate', handlePopState);
}

function handlePopState() {
  try {
    hasNavigatedAway = true;

    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'disconnect' }));
      ws.close();
    }

    cleanupGameResources();
  } catch (error) {
    console.error('Error in handlePopState:', error);
  }
}

function sendKeyEvent(key, isPressed) {
  try {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(
        JSON.stringify({ type: 'key_event', key, is_pressed: isPressed })
      );
    }
  } catch (error) {
    console.error('Error in sendKeyEvent:', error);
  }
}

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/game/')
) {
  try {
    await initGame();
  } catch (error) {
    showErrorToast(`Error initializing the game: ${error}`);
  }
}
