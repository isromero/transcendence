import { profileService } from '../services/profile.js';
import { usersService } from '../services/users.js';
import { IMAGES_URL } from '../utils/constants.js';

export function init() {
  const avatar = document.getElementById('avatar');
  const username = document.getElementById('username');
  const wins = document.getElementById('wins');
  const loses = document.getElementById('loses');
  const total = document.getElementById('total');
  const tournamentWins = document.getElementById('tournament-wins');
  const tournamentLoses = document.getElementById('tournament-loses');
  const onlineStatus = document.getElementById('online-status');
  const onlineIndicator = document.getElementById('online-indicator');
  const matchesContainer = document.getElementById('matches-container');

  function formatMatchType(type) {
    if (!type) return 'Unknown';

    const mapping = {
      local: 'Local',
      'tournament semi': 'Tournament Semifinals',
      'tournament final': 'Tournament Finals',
      'tournament group': 'Tournament Group Stage',
      ranked: 'Ranked Match',
      friendly: 'Friendly Match',
    };

    return mapping[type.toLowerCase()] || type;
  }

  async function loadProfileData() {
    const pathParts = window.location.pathname.split('/');
    const userId = pathParts[2];

    const { data } = userId
      ? await usersService.getUser(userId) // Perfil de un amigo
      : await profileService.getProfile(); // Perfil propio

    avatar.src = data.avatar
      ? `${IMAGES_URL}${data.avatar.replace('/images/', '/')}`
      : `${IMAGES_URL}/default_avatar.webp`;

    username.textContent = data.username;
    onlineStatus.textContent = data.is_online ? 'Online' : 'Offline';
    onlineIndicator.className = `text-${data.is_online ? 'success' : 'secondary'} me-1`;

    wins.textContent = Number(data.victories || 0);
    loses.textContent = Number(data.defeats || 0);
    total.textContent = Number(data.total_matches || 0);
    tournamentWins.textContent = Number(data.tournaments_victories || 0);
    tournamentLoses.textContent = Number(data.tournaments_defeats || 0);

    matchesContainer.innerHTML = '';
    if (Array.isArray(data.match_history)) {
      data.match_history.forEach(match => {
        const matchElement = document.createElement('div');
        matchElement.className = 'match-card';

        const date = new Date(match.date);
        const formattedDate = date.toLocaleDateString();
        const formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        matchElement.innerHTML = `
          <div class="match-info">
            <p><strong>${formatMatchType(match.type)}</strong></p>
            <p>${formattedDate} at ${formattedTime}</p>
            <p><strong>${data.username}</strong> ${match.score.user} - ${match.score.opponent} <strong>${match.opponent.username}</strong></p>
          </div>
        `;

        matchesContainer.appendChild(matchElement);
      });
    } else {
      matchesContainer.innerHTML = '<p>No matches found.</p>';
    }
  }

  loadProfileData();

  return () => {};
}
