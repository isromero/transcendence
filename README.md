# trascendence

## Requirements (major/minor modules chosen and more)
https://arc.net/e/059DF97D-3F04-49D1-A61C-EE5878BE8AB6

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
