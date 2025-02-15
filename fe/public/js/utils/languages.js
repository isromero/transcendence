let translations = null;

async function loadTranslations() {
  try {
    const response = await fetch('/assets/translations.json');
    translations = await response.json();
  } catch (error) {
    console.error('Error loading translations:', error);
  }
}

function setHTMLLang(lang) {
  document.documentElement.lang = lang;
}

export async function changeLanguage(lang) {
  if (!translations) {
    await loadTranslations();
  }

  const langMap = {
    es: 'spanish',
    en: 'english',
    'uk-UA': 'ukrainian',
  };

  setHTMLLang(lang);
  updateTranslations(langMap[lang]);
  localStorage.setItem('selectedLanguage', lang);
}

window.changeLanguage = changeLanguage;

function updateTranslations(currentLanguage) {
  document.querySelectorAll('[data-translationKey]').forEach(el => {
    const key = el.getAttribute('data-translationKey');
    if (translations[key] && translations[key][currentLanguage]) {
      const newText = translations[key][currentLanguage];

      if (
        el.tagName.toLowerCase() === 'input' &&
        ['button', 'submit', 'reset'].includes(el.type.toLowerCase())
      ) {
        el.value = newText;
      } else if (el.tagName.toLowerCase() === 'img') {
        el.alt = newText;
      } else {
        el.textContent = newText;
      }
    }
  });
}

window.addEventListener('load', () => {
  const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
  changeLanguage(savedLanguage);
});

document.querySelectorAll('[data-translationKey]').forEach(button => {
  button.addEventListener('click', event => {
    const lang = event.target.getAttribute('data-translationKey');
    changeLanguage(lang);
  });
});
