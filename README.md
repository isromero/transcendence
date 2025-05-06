# transcendence

## Project Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 20.0.0 or higher
- VS Code with recommended extensions (for linting and formatting)
- Black formatter (`pip install black`) if you want to use it locally
- Flake8 (`pip install flake8`) if you want to use it locally

### Development Environment
1. Clone the repository
2. Create environment files in fe/.env and be/.env (see .env.example)
3. Run docker compose build
4. Run docker compose up

### Virtual Environment be/
It's not necessary to create a virtual environment in be/ but if you want to have it because linting and formatting is easier + VS Code can suggest you the imports.

If not you can work inside the container and that's it.

Inside be/ folder do this:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Migrations
We don't use a virtual environment so you will need to run the migrations in the container.

```bash
docker compose run --rm be python manage.py makemigrations
docker compose run --rm be python manage.py migrate
```

### Services
The services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3001
- Database: http://localhost:5432

### Linting and Formatting VS Code
Intall the following extensions:
- ESLint
- Prettier
- Black Formatter -> ms-python.black-formatter
- Flake8 -> ms-python.flake8 (you will need to install flake8 locally)

### Linting and Formatting NEOVIM  
See [More on vim Linting](./fe/vim.md)

### Frontend Code Quality Tools inside fe/
#### ESLint
- Lints JavaScript, HTML and CSS files
- Run: `npm run lint`
- Fix: `npm run lint:fix`

#### Prettier
- Formats JavaScript, HTML and CSS files
- Run: `npm run format`
- Check: `npm run format:check`

#### Combined Commands
- Check all: `npm run check`
- Fix all: `npm run fix`

### Backend Code Quality Tools inside be/
#### Black (Formatter)
- Format all files: `black .`
- Check format: `black . --check`

#### Flake8 (Linter)
- Check all files: `flake8`

## Commits and branch names

In this project, we follow the Conventional Commits specification for structuring our commit messages and branch names. It enables automated tools and processes to analyze and generate release notes, changelogs, and versioning information. For more info on Conventional Commits, visit <https://www.conventionalcommits.org/en/v1.0.0/>

### Commit Message Format

Each commit message follows a specific format:

```code
<type>(<scope>): <subject>
```

`<type>`: Describes the purpose or nature of the commit. It can be one of the following values: `feat, fix, docs, style, refactor, test, chore, perf`.

`<scope>` (optional): Specifies the part of the project or component the commit affects. It can be a module, file, or a broader area of impact.

`<subject>`: A concise and clear description of the change. It should be written in the imperative mood, starting with a capital letter and without ending punctuation.

#### Examples of valid commit messages

```code
fix(authentication): Resolve login issue on Safari
feat(files): Add file upload feature
perf: Update dependencies to latest versions
```

### Branch Names

When creating branch names, we follow the same conventions as commit messages to maintain consistency and clarity

#### Examples of branch names

```code
feat/file-upload
fix/authentication-safari-login-issue
perf/bump-dependencies
```
