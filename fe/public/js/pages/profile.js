const form = document.getElementById('username');
const wins = document.getElementById('wins');
const loses = document.getElementById('loses');
const total = document.getElementById('total');
import { API_URL } from '../utils/constants.js';
import { showErrorToast, showSuccessToast } from '../utils/helpers.js';

  (async function() {
    const response = await fetch(`${API_URL}/stats/1`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const result = await response.json();

    if (!response.ok || !result?.success) {
      showErrorToast(result?.message || result?.error);
      return null;
    }
    console.log(result);
    form.textContent = result.data.username;
    wins.textContent = wins.textContent + ": " + (result.data.tournaments_victories + result.data.victories);
    loses.textContent = loses.textContent + ": " + (result.data.total_matches - (result.data.tournaments_victories + result.data.victories));
    total.textContent = total.textContent + ": " + (result.data.total_matches);
  })();