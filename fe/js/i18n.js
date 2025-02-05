const translations = {
    en: {
        login: "Login",
        signup: "Sign Up",
    },
    es: {
        login: "Iniciar Sesión",
        signup: "Registrarse",
    }
};

function updateText() {
    document.querySelectorAll("[data-i18n]").forEach(element => {
        const key = element.getAttribute("data-i18n");
        element.textContent = translations[currentLang][key];
    });
}

let currentLang = localStorage.getItem("language") || "en"; // Idioma por defecto

function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem("language", lang);
    updateText();
}

// Actualizar texto al cargar la página
document.addEventListener("DOMContentLoaded", updateText);
