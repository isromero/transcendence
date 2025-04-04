import { init as initLogin } from './pages/login.js';
import { init as initRegister } from './pages/register.js';
import { init as initProfile } from './pages/profile.js';
import { init as initFriends } from './pages/friends.js';
import { init as initRequests } from './pages/requests.js';

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
    SETTINGS
  */
};
