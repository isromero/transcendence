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

function updateTranslations(currentLanguage) {
  document.querySelectorAll('[data-translationKey]').forEach(el => {
    const key = el.getAttribute('data-translationKey');
    if (translations[key] && translations[key][currentLanguage]) {
      const newText = translations[key][currentLanguage];

      if (
        el.tagName.toLowerCase() === 'input' &&
        ['button', 'submit', 'reset'].includes(el.type.toLowerCase())
      ) {
        el.setAttribute('aria-label', newText);
        el.value = newText;
      } else if (el.tagName.toLowerCase() === 'img') {
        el.setAttribute('aria-label', newText);
        el.alt = newText;
      } else {
        el.setAttribute('aria-label', newText);
        el.textContent = newText;
      }
    }
  });
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

export function init() {
  const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
  changeLanguage(savedLanguage);

  async function handleLanguageClick(event) {
    const button = event.target.closest('button');
    if (!button) {
      return;
    }

    const lang = button.dataset.language;
    if (lang) {
      await changeLanguage(lang);
    }
  }

  document.addEventListener('click', handleLanguageClick);

  return () => {
    document.removeEventListener('click', handleLanguageClick);
  };
}
