import { init as initLogin } from './pages/login.js';
import { init as initRegister } from './pages/register.js';
import { init as initProfile } from './pages/profile.js';
import { init as initFriends } from './pages/friends.js';
import { init as initRequests } from './pages/requests.js';
import { init as initEditProfile } from './pages/editProfile.js';
import { init as initEditUsername } from './pages/editUsername.js';
import { init as initEditPassword } from './pages/editPassword.js';
import { init as initAccountDeletion } from './pages/accountDeletion.js';
import { init as initLanguages } from './pages/languages.js';
import { init as initLogout } from './pages/logout.js';

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
  '/friends': {
    init: initFriends,
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
};
