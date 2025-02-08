/*
 * setLanguage(newLang)
 * Changes the global language and updates all texts on the page.
 */
export function setLanguage(newLang) {
  csvToTranslations(csvData);
  const currentLanguage = newLang;
  updateTranslations(currentLanguage);
}

/**
 * Converts a CSV string into a translations object.
 * The CSV should have a header row with columns like:
 * key,english,spanish,ukranian,...
 *
 * @param {string} csvString - The CSV data as a string.
 * @returns {Object} An object mapping keys to their language translations.
 */
function csvToTranslations(csvString) {
  const lines = csvString
    .trim()
    .split('\n')
    .filter(line => line.trim() !== '');
  const headers = lines[0].split(',').map(header => header.trim());
  const translations = {};

  for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split(',').map(part => part.trim());
    const key = parts[0];
    translations[key] = {};
    for (let j = 1; j < headers.length; j++) {
      const lang = headers[j].toLowerCase(); // e.g., "english", "spanish"
      translations[key][lang] = parts[j] || '';
    }
  }
  console.log(translations);
  return translations;
}

const csvData = `
key,english,spanish,ukrainian
edit-username,Username,Nombre de usuario,Ім'я користувача
edit-mail,Email,Correo electrónico,Електронна пошта
finish-login,Account Deletion,Eliminación de cuenta,Видалення акаунта
Type-password,Type password,Escribe la contraseña,Введіть пароль
account-deletion-info,Account deletion info,Información sobre la eliminación de la cuenta,Інформація про видалення акаунта
learn-gdpr,Learn about GDPR,Aprender sobre GDPR,Дізнайтеся про GDPR
cancel,Cancel,Cancelar,Скасувати
accept,Accept,Aceptar,Прийняти
username,Username:,Usuario:,Ім'я користувача:
disabled,this is disabled,esto está deshabilitado,це відключено
data-deletion-info,Data deletion info,Información sobre la eliminación de datos,Інформація про видалення даних
new-password,New password,Nueva contraseña,Новий пароль
repeat-password,Repeat password,Repite la contraseña,Повторіть пароль
new-username,New username,Nuevo usuario,Нове ім'я користувача
forgot-password,I forgot my password,Olvidé mi contraseña,Я забув свій пароль
match-ended,MATCH ENDED,PARTIDA TERMINADA,МАТЧ ЗАВЕРШЕНО
winner,WINNER,GANADOR,ПЕРЕМОЖЕЦЬ
spectate,Spectate,Espectar,Спостерігати
return-menu,Return to Menu,Volver al Menú,Повернутися до меню
play-again,Play Again,Jugar de nuevo,Грати знову
tournament,Tournament,Torneo,Турнір
round-1,Round nº 1,Ronda nº 1,Раунд № 1
match,Match:,Partido:,Матч:
prev,Prev,Anterior,Попередній
next,Next,Siguiente,Наступний
exit,Exit,Salir,Вийти
waiting-players,Waiting Players,Esperando jugadores,Очікування гравців
code,Code:,Código:,Код:
new-email,New email,Nuevo correo,Нова електронна пошта
spanish,Español名,Español,Іспанська
english,English,Inglés,Англійська
login,Login,Iniciar sesión,Увійти
enter-code,Enter the code sent to:,Ingrese el código enviado a:,Введіть код, надісланий на:
enter-code-field,Enter code:,Ingrese código:,Введіть код:
sign-up,Sign Up,Registrarse,Зареєструватися
transcendence,Transcendence,Trascendencia,Трансцендентність
local,Local,Local,Локально
multiplayer,Multiplayer,Multijugador,Мультиплеєр
password,Password,Contraseña,Пароль
data-deletion,Data Deletion,Eliminación de datos,Видалення даних
account-deletion,Account Deletion,Eliminación de cuenta,Видалення акаунта
friends,Friends,Amigos,Друзі
new-friend,New Friend,Nuevo amigo,Новий друг
create-match,Create match,Crear partida,Створити матч
join-match,Join match,Unirse a partida,Приєднатися до матчу
num-players,Nº of players,Nº de jugadores,Кількість гравців
points-win,Points to win,Puntos para ganar,Очки для перемоги
register,Register,Registrarse,Зареєструватися
email-address,Email address,Dirección de correo,Електронна адреса
edit-profile,Edit profile,Editar perfil,Редагувати профіль
language,Language,Idioma,Мова
my-profile,My profile,Mi perfil,Мій профіль
wins,Wins:1,Victorias:1,Перемоги:1
loses,Loses:1,Derrotas:1,Поразки:1
total,Total:1,Total:1,Загалом:1
`;

/**
 * translate(key)
 * Returns the translation for a given key in the current language.
 */
function translate(key, currentLanguage) {
  const translations = csvToTranslations(csvData);

  if (translations[key] && translations[key][currentLanguage.toLowerCase()]) {
    return translations[key][currentLanguage.toLowerCase()];
  }
  return key;
}

/**
 * updateTranslations()
 * Finds every element marked with data-i18n and updates its text (or attribute)
 * according to the currentLanguage.
 */
function updateTranslations(currentLanguage) {
  const list = document.querySelectorAll('[data-i18n]');

  console.log(list);
  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    const key = el.getAttribute('data-i18n');
    const newText = translate(key, currentLanguage);

    // Decide which property to update:
    if (
      el.tagName.toLowerCase() === 'input' &&
      ['button', 'submit', 'reset'].includes(el.type.toLowerCase())
    ) {
      el.value = newText;
    } else if (el.tagName.toLowerCase() === 'img' && el.hasAttribute('alt')) {
      el.alt = newText;
    } else if (el.hasAttribute('aria-label')) {
      el.setAttribute('aria-label', newText);
      if (el.textContent.trim() !== '') {
        el.textContent = newText;
      }
    } else {
      el.textContent = newText;
    }
  });
}
