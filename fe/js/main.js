const appContainer = document.getElementById('app-container');
const pageContainer = document.getElementById('page-container');
const modalContainer = document.getElementById('modal-container');
const menuContainer = document.getElementById('menu-container');

async function loadPage(page) {
	let url;

	if (page.includes("menu-"))
	{
		url = '/pages/menus${page}.html';
		loadMenu(url);
	}
	else if (page.includes("game-"))
	{
		url = '/pages/game${page}.html';
		loadGame(url);
	}
	else if (page.includes("modal-"))
	{
		url = '/components${page}.html';
		loadModal(url);
	}
	else
	{
		url = '/components${page}.html';
		loadError(url);
	}
}

async function loadMenu(page) {
  try {
	const url = page;
    const response = await fetch(url);

	if (!response.ok)
	{
		/* TODO(samusanc): here goes an error checker for debug and other stuff, throw 
		 * exception is a mistake!!!*/
		throw new Error('Menu page not found');
	}

    const content = await response.text();
    pageContainer.innerHTML = content;

    //window.history.pushState({ page }, '', page);
    //updateIcons(page);

  } catch (error) {
    pageContainer.innerHTML = '<div class="text-center"><h1>Unknow Error 404</h1><p>'error.message'</p></div>';
  }
}

async function loadGame(page) {
  try {
	const url = page;
    const response = await fetch(url);

	if (!response.ok)
	{
		/* TODO(samusanc): here goes an error checker for debug and other stuff, throw 
		 * exception is a mistake!!!*/
		throw new Error('Game page not found');
	}

    const content = await response.text();
    appContainer.innerHTML = content;

  } catch (error) {
	loadPage('/');
    pageContainer.innerHTML = '<div class="text-center"><h1>Unknow Error 404</h1><p>'error.message'</p></div>';
  }
}

async function loadModal(page) {
  try {
	const url = page;
    const response = await fetch(url);

	if (!response.ok)
	{
		/* TODO(samusanc): here goes an error checker for debug and other stuff, throw 
		 * exception is a mistake!!!*/
		throw new Error('Modal page not found');
	}

    const content = await response.text();
    modalContainer.innerHTML = content;

  } catch (error) {
    modalContainer.innerHTML = '<div class="text-center"><h1>Unknow Error 404</h1><p>'error.message'</p></div>';
  }
}

async function loadError(page) {
  try {
    const url = page;
    const response = await fetch(url);

	if (!response.ok)
	{
		/* TODO(samusanc): here goes an error checker for debug and other stuff, throw 
		 * exception is a mistake!!!*/
		throw new Error('Error page not found');
	}

    const content = await response.text();
    pageContainer.innerHTML = content;

    //window.history.pushState({ page }, '', page);
    //updateIcons(page);

  } catch (error) {
    pageContainer.innerHTML = '<div class="text-center"><h1>Unknow Error 404</h1><p>'error.message'</p></div>';
  }
}

/*
function updateIcons(page) {
  const leftButton = document.querySelector('.btn.position-absolute.bottom-0.start-0 i');
  const rightButton = document.querySelector('.btn.position-absolute.bottom-0.end-0 i');

  if (page === '/login') {

    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  } else if (page === '/register') {
    
    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  }
  else if (page === '/') {
    
    leftButton.className = 'bi bi-question-circle';
    rightButton.className = 'bi bi-globe'; 
  }
   else {

    leftButton.className = 'bi bi-person-circle';
    leftButton.parentElement.setAttribute('href', '/profile');
    rightButton.className = 'bi bi-list'; 
    rightButton.parentElement.setAttribute('href', '/settings');
  }
}
*/

document.body.addEventListener('click', (event) => {
  const link = event.target.closest('a.spa-link');
  if (link) {
    event.preventDefault();
    const page = link.getAttribute('lsp-loader');
    loadPage(page);
  }
});

window.addEventListener('popstate', (event) => {
  const page = event.state?.page || '/';
  loadPage(page);
});

loadPage(window.location.pathname);
