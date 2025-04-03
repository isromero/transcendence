import { init as initLogin } from './pages/login.js';

export const pageControllers = {
  /* Auth */
  '/auth/login': {
    init: initLogin,
  },
  '/auth/register': {
    init: () => {
      console.log('init');
    },
  },
  /* Home */
  '/': {
    init: () => {
      console.log('init');
    },
  },
};
