const appContainer = document.getElementById('app-container');

export async function loadMenu(page) {
  try {
    const templateResponse = await fetch('/pages/templates/menu.html');
    if (!templateResponse.ok) {
      throw new Error('Error loading menu template');
    }

    const templateContent = await templateResponse.text();
    appContainer.innerHTML = templateContent;

    const pageContainer = document.getElementById('page-container');
    const contentResponse = await fetch(page);
    if (!contentResponse.ok) {
      throw new Error('Error loading menu content');
    }

    const pageContent = await contentResponse.text();
    pageContainer.innerHTML = pageContent;
  } catch (error) {
    console.error('Menu error:', error);
  }
}
