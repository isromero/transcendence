import { profileService } from './services/profile.js';

export async function getProfile() {
  const { data } = await profileService.getProfile();

  const username = document.getElementById('username');
  const wins = document.getElementById('wins');
  const loses = document.getElementById('loses');
  const total = document.getElementById('total');

  username.textContent = data.username;

  const victories = Number(data.victories || 0);
  const tournamentVictories = Number(data.tournament_victories || 0);
  const defeats = Number(data.defeats || 0);
  const tournamentDefeats = Number(data.tournament_defeats || 0);
  const totalMatches = Number(data.total_matches || 0);
  const totalTournaments = Number(data.total_tournaments || 0);

  wins.textContent = victories + tournamentVictories;
  loses.textContent = defeats + tournamentDefeats;
  total.textContent = totalMatches + totalTournaments;
}

if (
  document.readyState !== 'loading' &&
  window.location.pathname.includes('/profile')
) {
  await getProfile();
}
