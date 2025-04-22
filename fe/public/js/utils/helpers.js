import { pageMappings } from '../router/routes.js';
import { IMAGES_URL } from './constants.js';

export function getCleanPageKey(requestedPath) {
  if (pageMappings[requestedPath]) {
    return requestedPath;
  }
  return (
    Object.keys(pageMappings).find(
      key => pageMappings[key] === requestedPath
    ) || requestedPath
  );
}

// Parse the HTML content and set it to the container
export function parseAndSetContent(container, htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');

  // Empty the current content
  container.innerHTML = '';

  // Transfer all nodes of the parsed content
  Array.from(doc.body.childNodes).forEach(node => {
    container.appendChild(node.cloneNode(true));
  });
}

// Global validation of forms
export function initGlobalValidation(root = document) {
  // Select all forms within the container we receive (by default, document)
  const forms = root.querySelectorAll('.needs-validation');

  forms.forEach(form => {
    // To avoid re-initializing a form that already has listeners:
    if (!form.dataset.validationInitialized) {
      form.dataset.validationInitialized = 'true';

      form.addEventListener(
        'submit',
        event => {
          event.preventDefault();
          if (!form.checkValidity()) {
            event.stopPropagation();
            form.classList.add('was-validated');
            return;
          }
          // Emit a custom event if it is valid
          form.dispatchEvent(
            new CustomEvent('formValid', { bubbles: true, cancelable: true })
          );
        },
        false
      );
    }
  });
}

export function showSuccessToast(message) {
  const toastEl = document.getElementById('successToast');
  toastEl.querySelector('.toast-body').textContent = message;
  const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
  toast.show();
}

export function showErrorToast(result) {
  const toastEl = document.getElementById('errorToast');
  let message;

  if (typeof result === 'string') {
    message = result;
  } else if (result.error) {
    if (typeof result.error === 'string') {
      message = result.error;
    } else if (result.error.type === 'validation_error') {
      // Handle form validation errors
      const errors = result.error.fields;

      // If there is a general error (__all__), use that message directly
      if (errors.__all__) {
        message = errors.__all__;
      } else {
        // If there are specific field errors, show them with their fields
        message = Object.entries(errors)
          .map(([field, msg]) => `${field}: ${msg}`)
          .join('\n');
      }
    } else if (result.error.__all__) {
      // Handle case where error is an object with __all__ directly
      message = Array.isArray(result.error.__all__)
        ? result.error.__all__[0]
        : result.error.__all__;
    } else {
      // Handle simple error messages
      message = result.error.message || 'An error occurred';
    }
  } else {
    message = 'An error occurred';
  }

  const messageEl = toastEl.querySelector('.toast-body');
  messageEl.innerHTML = message.replace(/\n/g, '<br>');
  const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
  toast.show();
}

const updateMatchResults = (roundMatches, roundPrefix) => {
  roundMatches.forEach(match => {
    const matchNumber = match.tournament_match_number;
    const player1 = match.player1;
    const player2 = match.player2;

    // Update scores
    const player1Score = document.querySelector(
      `.${roundPrefix}-player${matchNumber * 2 - 1}`
    );
    const player2Score = document.querySelector(
      `.${roundPrefix}-player${matchNumber * 2}`
    );

    if (player1Score && player2Score) {
      player1Score.textContent = player1.score || '0';
      player2Score.textContent = player2.score || '0';
    }

    // Update player information using IDs
    const p1Name = document.getElementById(
      `${roundPrefix}${matchNumber}-p1-name`
    );
    const p1Img = document.getElementById(
      `${roundPrefix}${matchNumber}-p1-img`
    );
    const p2Name = document.getElementById(
      `${roundPrefix}${matchNumber}-p2-name`
    );
    const p2Img = document.getElementById(
      `${roundPrefix}${matchNumber}-p2-img`
    );

    if (p1Name) {
      p1Name.textContent = player1.username;
    }
    if (p2Name) {
      p2Name.textContent = player2.username;
    }

    if (p1Img) {
      p1Img.src = player1.avatar
        ? `${IMAGES_URL}${player1.avatar.replace('/images/', '/')}`
        : `${IMAGES_URL}/default_avatar.webp`;
    }
    if (p2Img) {
      p2Img.src = player2.avatar
        ? `${IMAGES_URL}${player2.avatar.replace('/images/', '/')}`
        : `${IMAGES_URL}/default_avatar.webp`;
    }
  });
};

export function updateTournamentUI(tournamentData) {
  const tournamentName = document.getElementById('tournament-name');
  const joinCode = document.getElementById('join-code');
  const lang = document.documentElement.lang;

  tournamentName.textContent = tournamentData.tournament_name;
  if (lang === 'uk-UA') {
    joinCode.textContent = `Код приєднання: ${tournamentData.join_code}`;
  }
  if (lang === 'es') {
    joinCode.textContent = `Código de partida: ${tournamentData.join_code}`;
  }
  if (lang === 'en') {
    joinCode.textContent = `Join Code: ${tournamentData.join_code}`;
  }

  const playerSlots = document.querySelectorAll('.player-info span');
  playerSlots.forEach(slot => {
    if (lang === 'uk-UA') {
      slot.textContent = 'Очікування гравця...';
    }
    if (lang === 'es') {
      slot.textContent = 'Esperando Jugador...';
    }
    if (lang === 'en') {
      slot.textContent = 'Waiting for player...';
    }
    slot.previousElementSibling.src = `${IMAGES_URL}/default_avatar.webp`;
  });

  const playerSlots2 = document.querySelectorAll('.player-info-final span');
  playerSlots2.forEach(slot => {
    if (lang === 'uk-UA') {
      slot.textContent = 'Очікування гравця...';
    }
    if (lang === 'es') {
      slot.textContent = 'Esperando Jugador...';
    }
    if (lang === 'en') {
      slot.textContent = 'Waiting for player...';
    }
    slot.previousElementSibling.src = `${IMAGES_URL}/default_avatar.webp`;
  });

  const winnerImage = document.getElementById('winner-avatar');

  winnerImage.src = `${IMAGES_URL}/default_avatar.webp`;

  if (Array.isArray(tournamentData.players)) {
    tournamentData.players.forEach((player, index) => {
      if (playerSlots[index]) {
        playerSlots[index].textContent = player.username;
        playerSlots[index].previousElementSibling.src =
          `${IMAGES_URL}${player.avatar.replace('/images/', '/')}` ||
          `${IMAGES_URL}/default_avatar.webp`;
      }
    });
  }

  if (tournamentData.matches.quarter_finals?.length > 0) {
    updateMatchResults(tournamentData.matches.quarter_finals, 'quarter');
  }

  if (tournamentData.matches.semi_finals?.length > 0) {
    updateMatchResults(tournamentData.matches.semi_finals, 'semi');
  }

  if (tournamentData.matches.finals?.length > 0) {
    updateMatchResults(tournamentData.matches.finals, 'final');
  }

  if (tournamentData.matches.finals?.length > 0) {
    const finalMatch = tournamentData.matches.finals[0];
    const player1 = finalMatch.player1;
    const player2 = finalMatch.player2;

    // Update final match information using IDs
    const p1Name = document.getElementById('final-p1-name');
    const p1Img = document.getElementById('final-p1-img');
    const p2Name = document.getElementById('final-p2-name');
    const p2Img = document.getElementById('final-p2-img');
    const p1Score = document.querySelector('.final-player1');
    const p2Score = document.querySelector('.final-player2');

    if (p1Name) {
      p1Name.textContent = player1.username;
    }
    if (p2Name) {
      p2Name.textContent = player2.username;
    }
    if (p1Score) {
      p1Score.textContent = player1.score || '0';
    }
    if (p2Score) {
      p2Score.textContent = player2.score || '0';
    }

    if (p1Img) {
      p1Img.src = player1.avatar
        ? `${IMAGES_URL}${player1.avatar.replace('/images/', '/')}`
        : `${IMAGES_URL}/default_avatar.webp`;
    }
    if (p2Img) {
      p2Img.src = player2.avatar
        ? `${IMAGES_URL}${player2.avatar.replace('/images/', '/')}`
        : `${IMAGES_URL}/default_avatar.webp`;
    }

    // Update winner if the game is finished
    if (Math.max(player1.score, player2.score) >= 5) {
      const winner = player1.score > player2.score ? player1 : player2;
      const winnerImage = document.getElementById('winner-avatar');
      const winnerName = document.getElementById('winner-name');

      if (winnerImage && winnerName) {
        winnerImage.src = winner.avatar
          ? `${IMAGES_URL}${winner.avatar.replace('/images/', '/')}`
          : `${IMAGES_URL}/default_avatar.webp`;
        winnerName.textContent = winner.username;
      }
    }
  }
}
