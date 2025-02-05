// Global variable for translations
let translations = {};

// Función para cargar las traducciones desde el archivo JSON
async function loadTranslations() {
    try {
        const response = await fetch("js/translations.json"); // Ruta al archivo JSON
        if (!response.ok) {
            throw new Error('Error loading translations');
        }
        translations = await response.json(); // Cargar las traducciones
    } catch (error) {
        console.error("Error loading translations:", error);
    }
}

// Función para actualizar el texto de los elementos en la página
function updateText() {
    document.querySelectorAll("[data-i18n]").forEach(element => {
        const key = element.getAttribute("data-i18n");
        const lang = localStorage.getItem("language") || "en"; // Obtener el idioma del localStorage
        const translatedText = translations[lang][key];
        if (translatedText) {
            element.textContent = translatedText;
        }
    });
}

// Función para cambiar el idioma
function changeLanguage(lang) {
    localStorage.setItem("language", lang); // Guardar el idioma en localStorage
    updateText(); // Actualizar los textos con el nuevo idioma
}

// Función para inicializar la página con las traducciones
document.addEventListener("DOMContentLoaded", async function() {
    await loadTranslations(); // Cargar las traducciones
    const savedLanguage = localStorage.getItem("language");
    const lang = savedLanguage ? savedLanguage : "en"; // Usar idioma guardado o "en" por defecto
    changeLanguage(lang); // Aplicar el idioma
});
