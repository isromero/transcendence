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

  async function loadProfileData() {
    const pathParts = window.location.pathname.split('/');
    const userId = pathParts[2];

    const { data } = userId
      ? await usersService.getUser(userId)
      : await profileService.getProfile();

    avatar.src = data.avatar
      ? `${IMAGES_URL}${data.avatar.replace('/images/', '/')}`
      : `${IMAGES_URL}/default_avatar.webp`;

    username.textContent = data.username;

    const victories = Number(data.victories || 0);
    const tournamentVictories = Number(data.tournament_victories || 0);
    const defeats = Number(data.defeats || 0);
    const tournamentDefeats = Number(data.tournament_defeats || 0);
    const totalMatches = Number(data.total_matches || 0);

    wins.textContent = victories;
    loses.textContent = defeats;
    total.textContent = totalMatches;
    tournamentWins.textContent = tournamentVictories;
    tournamentLoses.textContent = tournamentDefeats;
  }

  loadProfileData();

  return () => {};  return () => {};
}
