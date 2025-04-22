import prettier from 'eslint-plugin-prettier';
import promise from 'eslint-plugin-promise';
import html from 'eslint-plugin-html';
import globals from 'globals';
import cssPlugin from 'eslint-plugin-css';
export default [
  cssPlugin.configs['flat/recommended'],
  {
    files: ['**/*.js', '**/*.cjs', '**/*.mjs', '**/*.html'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.es2022,
        bootstrap: 'readonly',
      },
    },
    plugins: {
      prettier,
      promise,
      html,
    },
    rules: {
      // Basic error prevention
      'no-console': ['warn', { allow: ['error'] }], // Warns when console.* is used except for console.error
      'no-debugger': 'warn', // Warns when debugger statements are used
      'no-duplicate-case': 'error', // Prevents duplicate case labels in switch statements
      'no-irregular-whitespace': 'error', // Prevents irregular whitespace outside of strings
      'no-unreachable': 'error', // Prevents unreachable code after return, throw, continue, and break
      'no-constant-binary-expression': 'error', // Prevents expressions that always result in the same value
      'no-var': 'error', // Requires let or const instead of var
      'no-unused-vars': 'warn', // Warns about variables that are declared but never used
      'no-undef': 'error', // Prevents usage of undeclared variables
      'no-empty': 'warn', // Warns about empty block statements

      // Good practices
      'prefer-const': 'warn', // Suggests using const for variables that are never reassigned
      eqeqeq: ['error', 'always'], // Requires === and !== instead of == and !=
      curly: ['error', 'all'], // Requires curly braces for all control statements
      'no-else-return': 'warn', // Suggests removing else when if block contains a return
      'no-unused-expressions': 'error', // Prevents unused expressions that don't affect program state
      'prefer-template': 'warn', // Suggests using template literals instead of string concatenation
      'arrow-body-style': ['warn', 'as-needed'], // Suggests simpler arrow function syntax when possible

      // Array and object best practices
      'array-callback-return': 'error', // Enforces return statements in array method callbacks
      'object-shorthand': 'warn', // Suggests using shorthand syntax for object properties
      'prefer-spread': 'warn', // Suggests using spread operator instead of .apply()

      // Async/Await rules
      'promise/prefer-await-to-then': 'error', // Prohibits .then() and forces use of await
      'promise/prefer-await-to-callbacks': 'error', // Prefers await over callbacks
      'no-async-promise-executor': 'error', // Prevents async in new Promise
      'require-await': 'error', // Requires that async functions use await
      'no-await-in-loop': 'warn', // Warns about possible optimizations in loops with await
      'max-nested-callbacks': ['error', 3], // Limits the nesting of callbacks

      // Code formatting
      'prettier/prettier': 'error', // Enforces consistent code formatting using Prettier
    },
  },
];
