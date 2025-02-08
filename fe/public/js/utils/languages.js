import { setLanguage } from './test.js';

function setHTMLLang(lang) {
  document.documentElement.lang = lang;
}

function changeLanguage(lang) {
  if (lang === 'es') {
    setHTMLLang('es');
  }
  if (lang === 'en') {
    setHTMLLang('en');
  }
  if (lang === 'uk-UA') {
    setHTMLLang('uk-UA');
  }
  setLanguage();
}

window.changeLanguage = changeLanguage;
