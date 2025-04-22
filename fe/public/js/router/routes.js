export const pageMappings = {
  // Pages (user routes)
  '': '/pages/menus/home.html',
  '/auth': '/pages/menus/auth.html',
  '/auth/login': '/pages/menus/login.html',
  '/auth/register': '/pages/menus/register.html',
  '/auth/privacy': '/pages/menus/privacy_policy.html',
  '/auth/help': '/pages/menus/rickroll.html',
  '/create-match': '/pages/menus/create-match.html',
  '/join-tournament': '/pages/menus/join-tournament.html',
  '/tournament-settings': '/pages/menus/tournament-settings.html',
  '/profile': '/pages/menus/profile.html',
  '/profile/:id': '/pages/menus/profile.html',
  '/edit-profile': '/pages/menus/edit-profile.html',
  '/social': '/pages/menus/social.html',
  '/friends': '/pages/menus/friends.html',
  '/requests': '/pages/menus/requests.html',
  '/settings': '/pages/menus/settings.html',
  '/game/:id': '/pages/game/game.html',
  '/auth/privacy': '/pages/menus/privacy_policy.html',
  '/game/:id/tournament/:id': '/pages/game/game.html', // :id -> join_code
  '/tournament/:id': '/pages/menus/tournament.html', // :id -> join_code

  // Modals (no user routes)
  '/modal-account-deletion': '/pages/components/modals/account-deletion.html',
  '/modal-add-friend': '/pages/components/modals/add-friend.html',
  '/modal-data-deletion': '/pages/components/modals/data-deletion.html',
  '/modal-edit-password': '/pages/components/modals/edit-password.html',
  '/modal-edit-username': '/pages/components/modals/edit-username.html',
  '/modal-end-game-tournament':
    '/pages/components/modals/end-game-tournament.html',
  '/modal-end-game': '/pages/components/modals/end-game.html',
  '/modal-languages': '/pages/components/modals/languages.html',
  '/modal-login': '/pages/components/modals/login.html',
  '/modal-spectate-menu': '/pages/components/modals/spectate-menu.html',
  '/modal-waiting-screen': '/pages/components/modals/waiting-screen.html',
  '/modal-logout': '/pages/components/modals/logout.html',
};
