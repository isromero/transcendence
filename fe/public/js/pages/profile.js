import { profileService } from '../services/profile.js';
import { usersService } from '../services/users.js';
import { IMAGES_URL } from '../utils/constants.js';

export function init() {
  const avatar = document.getElementById('avatar');
  const username = document.getElementById('username');
  const wins = document.getElementById('wins');
  const loses = document.getElementById('loses');
  const total = document.getElementById('total');

  async function loadProfileData() {
    // Get the ID of the URL if it exists
    const pathParts = window.location.pathname.split('/');
    const userId = pathParts[2]; // /profile/123 -> 123

    const { data } = userId
      ? await usersService.getUser(userId)
      : await profileService.getProfile();

    // Update avatar
    avatar.src = data.avatar
      ? `${IMAGES_URL}${data.avatar.replace('/images/', '/')}`
      : `${IMAGES_URL}/default_avatar.webp`;

    // Update username
    username.textContent = data.username;

    // Calculate statistics
    const victories = Number(data.victories || 0);
    const tournamentVictories = Number(data.tournament_victories || 0);
    const defeats = Number(data.defeats || 0);
    const tournamentDefeats = Number(data.tournament_defeats || 0);
    const totalMatches = Number(data.total_matches || 0);
    const totalTournaments = Number(data.total_tournaments || 0);

    // Update statistics
    wins.textContent = victories + tournamentVictories;
    loses.textContent = defeats + tournamentDefeats;
    total.textContent = totalMatches + totalTournaments;
  }

  loadProfileData();

  return () => {};
}
