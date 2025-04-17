import { loadPage } from '../router/router.js';
import { showErrorToast, updateTournamentUI } from '../utils/helpers.js';
import { historyService } from '../services/history.js';
import { IMAGES_URL } from '../utils/constants.js';
import { tournamentService } from '../services/tournaments.js';
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

function isHorizontal() {
  if (window.innerWidth > window.innerHeight) {
    return true;
  }
  return false;
}

function updateGameRotation() {
  const rotatorElement = document.getElementById('rotator');
  const countdownElement = document.getElementById('countdown');

  if (!rotatorElement || !countdownElement) {
    return;
  }

  const angle = isHorizontal() ? 0 : 90;

  rotatorElement.style.transform = `rotate(${angle}deg)`;

  // For vertical orientation, handle countdown positioning and rotation
  if (!isHorizontal()) {
    // Position the countdown in the center of the screen
    countdownElement.style.transform = `rotate(-90deg)`;
    countdownElement.style.position = 'absolute';
    countdownElement.style.zIndex = '100';
    countdownElement.style.top = '50%';
    countdownElement.style.left = '50%';
    countdownElement.style.transform = 'translate(-50%, -50%) rotate(-90deg)';
  } else {
    // Reset all styles for horizontal orientation
    countdownElement.style.transform = '';
    countdownElement.style.position = '';
    countdownElement.style.zIndex = '';
    countdownElement.style.top = '';
    countdownElement.style.left = '';
  }
}

async function updateGameState(gameState) {
  // No need to call updateGameRotation here since it's already called during initialization
  // and will be handled by window resize event
  try {
    if (gameState.type === 'init' && gameState.state) {
      gameState = gameState.state;
    }

    if (gameEnded) {
      return;
    }

    const countdownElement = document.getElementById('countdown');
    if (countdownElement) {
      if (gameState.countdown !== null && gameState.countdown > 0) {
        countdownElement.style.display = 'block';
        countdownElement.textContent = Math.ceil(gameState.countdown);
      } else {
        countdownElement.style.display = 'none';
      }
    }

    if (!ctx) {
      return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const { left_paddle, right_paddle, ball, scores } = gameState;

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
    ctx.font = '40px Pixelify Sans';
    ctx.textAlign = 'center';
    ctx.fillText(`${scores.left} - ${scores.right}`, canvas.width / 2, 50);

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

        const tournamentData = await tournamentService.getTournament(joinCode);

        updateTournamentUI(tournamentData);
      } else {
        if (window.location.pathname.includes('game/')) {
          // If it's a multiplayer or local game, show the modal
          await loadPage('/modal-end-game');

          const matchId = path.split('/game/')[1]?.split('/')[0];
          const data = await historyService.getMatchHistory(matchId);

          setWinner(data);
        }
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

// Add window resize event to handle orientation changes
window.addEventListener('resize', updateGameRotation);
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

  const isLocalMatch = data.type_match === 'local';
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

    if (
      data &&
      data.status === 'finished' &&
      window.location.pathname.includes('game/')
    ) {
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

function setupMobileControls() {
  const buttonMapping = {
    'left-up': 'w',
    'left-down': 's',
    'right-up': 'ArrowUp',
    'right-down': 'ArrowDown',
  };
  

  Object.keys(buttonMapping).forEach(buttonId => {
    const button = document.getElementById(buttonId);
    if (!button) {
      return;
    }

    button.addEventListener('mousedown', () =>
      sendKeyEvent(buttonMapping[buttonId], true)
    );
    button.addEventListener('mouseup', () =>
      sendKeyEvent(buttonMapping[buttonId], false)
    );

    button.addEventListener('touchstart', e => {
      e.preventDefault();
      sendKeyEvent(buttonMapping[buttonId], true);
    });

    button.addEventListener('touchend', e => {
      e.preventDefault();
      sendKeyEvent(buttonMapping[buttonId], false);
    });
  });
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

export function init() {
  // Prevent multiple simultaneous initializations
  if (isInitializing) {
    return;
  }

  isInitializing = true;

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

  async function handlePopState() {
    try {
      hasNavigatedAway = true;

      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'disconnect' }));
        ws.close();
      }

      cleanupGameResources();

      const path = window.location.pathname;
      const matchId = path.split('/game/')[1]?.split('/')[0];

      if (matchId) {
        const gameFinished = await checkIfGameFinished(matchId);
        if (gameFinished) {
          await loadPage('/');
          return;
        }
      }
    } catch (error) {
      console.error('Error en handlePopState:', error);
    }
  }

  function cleanupGameResources() {
    stopGame();
    document.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('keyup', handleKeyUp);
    window.removeEventListener('beforeunload', handleBeforeUnload);
    window.removeEventListener('popstate', handlePopState);
  }

  async function initializeGame() {
    try {
      resetGameState();

      // Initialize canvas
      canvas = document.getElementById('pong');
      if (!canvas) {
        return;
      }

      ctx = canvas.getContext('2d');
      // Establece resolución interna sin forzar tamaño visual
      canvas.width = 800;
      canvas.height = 400;

      canvas.style.width = '100%';
      canvas.style.height = 'auto';

      const path = window.location.pathname;
      const matchId = path.split('/game/')[1]?.split('/')[0];

      if (!matchId) {
        console.error('No valid match ID found');
        return;
      }

      // Check if game is already finished
      const gameFinished = await checkIfGameFinished(matchId);
      if (gameFinished) {
        return;
      }

      if (!gameFinished) {
        await updateGameRotation();
      }

      // Initialize WebSocket
      ws = new WebSocket(
        `wss://${window.location.hostname}:8443/ws/game/${matchId}`
      );

      ws.onopen = () => {
        if (ws?.readyState === WebSocket.OPEN) {
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
          setTimeout(initializeGame, 1000);
        }
      };

      ws.onerror = error => {
        showErrorToast(`Error connecting to the game: ${error}`);
      };

      setupMobileControls();
    } catch (error) {
      console.error('Error in initializeGame:', error);
    }
  }

  document.addEventListener('keydown', handleKeyDown);
  document.addEventListener('keyup', handleKeyUp);
  window.addEventListener('beforeunload', handleBeforeUnload);
  window.addEventListener('popstate', handlePopState);
  window.addEventListener('resize', updateGameRotation);

  initializeGame();

  return () => {
    cleanupGameResources();
    window.removeEventListener('resize', updateGameRotation);
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'disconnect' }));
      ws.close();
    }
    isInitializing = false;
  };
}
