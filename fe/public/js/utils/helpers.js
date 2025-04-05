import { pageMappings } from '../router/routes.js';

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

// * Parse the HTML content and create script elements to be executed
// * This is ultra important to execute the scripts in a SPA
export function parseAndSetContent(container, htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');

  // Empty the current content
  container.innerHTML = '';

  // Transfer all nodes of the parsed content
  Array.from(doc.body.childNodes).forEach(node => {
    container.appendChild(node.cloneNode(true));
  });

  // Search and execute scripts
  const scripts = Array.from(container.querySelectorAll('script'));
  scripts.forEach(script => {
    const newScript = document.createElement('script');
    newScript.async = false; // Ensure scripts are executed in the order they appear
    newScript.type = 'module';
    if (script.src) {
      newScript.src = script.src;
    } else {
      newScript.textContent = script.textContent;
    }
    script.parentNode.replaceChild(newScript, script);
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

export function updateTournamentUI(tournamentData) {
  const tournamentName = document.getElementById('tournament-name');
  const joinCode = document.getElementById('join-code');

  tournamentName.textContent = tournamentData.tournament_name;
  joinCode.textContent = `Join Code: ${tournamentData.join_code}`;


  const playerSlots = document.querySelectorAll('.player-info span');
  playerSlots.forEach(slot => {
    slot.textContent = 'Waiting for player...';
    slot.previousElementSibling.src =
      '/public/assets/images/default-avatar.webp';
  });
  const playerSlots2 = document.querySelectorAll('.player-info-final span');
  playerSlots2.forEach(slot => {
    slot.textContent = 'Waiting for player...';
    slot.previousElementSibling.src =
      '/public/assets/images/default-avatar.webp';
  });


  if (Array.isArray(tournamentData.players)) {
    tournamentData.players.forEach((player, index) => {
      if (playerSlots[index]) {
        playerSlots[index].textContent = player.username;
        playerSlots[index].previousElementSibling.src =
          player.avatar || '/public/assets/images/default-avatar.webp';
      }
    });
  }


  const updateMatchResults = (roundMatches, roundPrefix, matchClassPrefix) => {
    roundMatches.forEach((match, index) => {
      const player1 = match.player1;
      const player2 = match.player2;
      const matchElements = document.querySelectorAll(`.${roundPrefix}-player${index * 2 + 1}, .${roundPrefix}-player${index * 2 + 2}`);
      const matchImages = document.querySelectorAll(`.${matchClassPrefix} .player-info img`);

      if (matchElements.length > 0 && matchImages.length > 0) {
        matchElements[0].textContent = player1.score;
        matchElements[1].textContent = player2.score;
        matchImages[0].src = player1.avatar || '/public/assets/images/default-avatar.webp';
        matchImages[1].src = player2.avatar || '/public/assets/images/default-avatar.webp';
      }
    });
  };


  if (tournamentData.matches.quarters) {
    updateMatchResults(tournamentData.matches.quarters, 'cuarter', 'match-result');
  }


  if (tournamentData.matches.semi_finals) {
    updateMatchResults(tournamentData.matches.semi_finals, 'semis', 'match-result');
  }


  if (tournamentData.matches.finals) {
    const finalMatch = tournamentData.matches.finals[0];
    const finalElements = document.querySelectorAll('.player-info-final span');
    const finalImages = document.querySelectorAll('.player-info-final img');

    if (finalMatch) {
      const finalPlayer1 = finalMatch.player1;
      const finalPlayer2 = finalMatch.player2;

      if (finalElements.length > 0 && finalImages.length > 0) {
        finalElements[0].textContent = finalPlayer1.username;
        finalElements[1].textContent = finalPlayer2.username;
        finalImages[0].src = finalPlayer1.avatar || '/public/assets/images/default-avatar.webp';
        finalImages[1].src = finalPlayer2.avatar || '/public/assets/images/default-avatar.webp';
      }

      const finalScores = document.querySelectorAll('.match-result span.text-warning');
      if (finalScores.length === 2) {
        finalScores[0].textContent = finalPlayer1.score;
        finalScores[1].textContent = finalPlayer2.score;
      }

      const winner = finalPlayer1.score > finalPlayer2.score ? finalPlayer1 : finalPlayer2;
      const winnerElement = document.querySelector('.final-winner .card-body');
      if (winnerElement) {
        const winnerImage = winnerElement.querySelector('img');
        const winnerName = winnerElement.querySelector('span');

        winnerImage.src = winner.avatar || '/public/assets/images/default-avatar.webp';
        winnerName.textContent = winner.username;
      }
    }
  }
}

