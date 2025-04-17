import { init as initLogin } from '../pages/login.js';
import { init as initRegister } from '../pages/register.js';
import { init as initProfile } from '../pages/profile.js';
import { init as initFriends } from '../pages/friends.js';
import { init as initRequests } from '../pages/requests.js';
import { init as initEditProfile } from '../pages/editProfile.js';
import { init as initEditUsername } from '../pages/editUsername.js';
import { init as initEditPassword } from '../pages/editPassword.js';
import { init as initAccountDeletion } from '../pages/accountDeletion.js';
import { init as initLanguages } from '../pages/languages.js';
import { init as initLogout } from '../pages/logout.js';
import { init as initCreateMatch } from '../pages/createMatch.js';
import { init as initTournamentSettings } from '../pages/tournamentSettings.js';
import { init as initTournament } from '../pages/tournament.js';
import { init as initJoinTournament } from '../pages/joinTournament.js';
import { init as initGame } from '../pages/game.js';
import { init as initAddFriend } from '../pages/addFriend.js';

export const pageControllers = {
  /* 
    AUTH
  */
  '/auth/login': {
    init: initLogin,
  },
  '/auth/register': {
    init: initRegister,
  },
  /*
    SOCIAL
  */
  '/profile': {
    init: initProfile,
  },
  '/profile/:id': {
    init: initProfile,
  },
  '/friends': {
    init: initFriends,
  },
  '/modal-add-friend': {
    init: initAddFriend,
  },
  '/requests': {
    init: initRequests,
  },
  /* 
    SETTINGS -> EDIT PROFILE
  */
  '/edit-profile': {
    init: initEditProfile,
  },
  '/modal-edit-username': {
    init: initEditUsername,
  },
  '/modal-edit-password': {
    init: initEditPassword,
  },
  '/modal-account-deletion': {
    init: initAccountDeletion,
  },
  /* 
    SETTINGS -> LANGUAGES
  */
  '/modal-languages': {
    init: initLanguages,
  },
  /* 
    SETTINGS -> LOGOUT
  */
  '/modal-logout': {
    init: initLogout,
  },
  /* 
    CREATE MATCH
  */
  '/create-match': {
    init: initCreateMatch,
  },
  /*
    CREATE MATCH -> TOURNAMENT SETTINGS
  */
  '/tournament-settings': {
    init: initTournamentSettings,
  },
  /*
    TOURNAMENT
  */
  '/tournament/:id': {
    init: initTournament,
  },
  /* 
    JOIN TOURNAMENT
  */
  '/join-tournament': {
    init: initJoinTournament,
  },
  /*
    GAME
  */
  '/game/:id': {
    init: initGame,
  },
  '/game/:id/tournament/:id': {
    init: initGame,
  },
};
