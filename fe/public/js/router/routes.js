export const pageMappings = {
  // Pages (user routes)
  '': '/pages/menus/home.html',
  '/auth': '/pages/menus/auth.html',
  '/auth/login': '/pages/menus/login.html',
  '/auth/register': '/pages/menus/register.html',
  '/create-match': '/pages/menus/create-match.html',
  '/join-match': '/pages/menus/join-match.html',
  '/match-settings': '/pages/menus/match-settings.html',
  '/match-settings-local': '/pages/menus/match-settings-local.html',
  '/profile': '/pages/menus/profile.html',
  '/edit-profile': '/pages/menus/edit-profile.html',
  '/social': '/pages/menus/social.html',
  '/friends': '/pages/menus/friends.html',
  '/settings': '/pages/menus/settings.html',
  '/game/:id': '/pages/game/game.html',

  '/tournament/:id': '/pages/menus/tournament.html',
  '/tournament-big': '/pages/menus/tournament-big.html',




  // Modals (no user routes)
  '/modal-account-deletion': '/pages/components/modals/account-deletion.html',
  '/modal-add-friend': '/pages/components/modals/add-friend.html',
  '/modal-data-deletion': '/pages/components/modals/data-deletion.html',
  // ! NOT USED BECAUSE WE DELETED EMAIL '/modal-edit-mail': '/pages/components/modals/edit-mail.html',
  '/modal-edit-password': '/pages/components/modals/edit-password.html',
  '/modal-edit-username': '/pages/components/modals/edit-username.html',
  '/modal-end-game-tournament':
    '/pages/components/modals/end-game-tournament.html',
  '/modal-end-game': '/pages/components/modals/end-game.html',
  '/modal-languages': '/pages/components/modals/languages.html',
  '/modal-login': '/pages/components/modals/login.html',
  '/modal-spectate-menu': '/pages/components/modals/spectate-menu.html',
  // ! NOT USED BECAUSE WE DELETED EMAIL '/modal-verify-email': '/pages/components/modals/verify-email.html',
  '/modal-waiting-screen': '/pages/components/modals/waiting-screen.html',
};
