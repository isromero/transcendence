# Setting Up Prettier, ESLint, Black, and Flake8 in VIM with Mason and LSP

## Introduction
This guide explains how to configure Prettier, ESLint, Black, and Flake8 in VIM using Mason and LSP. It provides installation instructions for both Vim-Plug and the most popular Vim package manager (Packer).

## Requirements
Ensure you have the following installed:
- Neovim (version 0.5+)
- Node.js (for ESLint, Prettier, and TypeScript)
- Python (for Black and Flake8)
- `pip`, `npm`, or `yarn` for installing language-specific tools

## Installing Mason and LSPs
Mason is a package manager for LSP servers, formatters, and linters. It simplifies installation and management.

### Installing Mason with Vim-Plug
Add the following lines to your `init.vim` or `init.lua`:

```lua
call('plug#begin', '~/.config/nvim/Plugged/')
Plug 'williamboman/mason.nvim'
Plug 'williamboman/mason-lspconfig.nvim'
Plug 'neovim/nvim-lspconfig'
call('plug#end')
```

Run the following command in Vim:
```
:PlugInstall
```

### Installing Mason with Packer
Add this to your `init.lua`:

```lua
return require('packer').startup(function()
  use 'williamboman/mason.nvim'
  use 'williamboman/mason-lspconfig.nvim'
  use 'neovim/nvim-lspconfig'
end)
```

Run the following command in Vim:
```
:PackerSync
```

## Configuring Mason and LSPs
Add this to your `init.lua`:

```lua
require('mason').setup({})
require('mason-lspconfig').setup({
  ensure_installed = {
    'cssls',
    'eslint',
    'html',
    'tsserver',
    'pylsp',
  },
  handlers = {
    function(server_name)
      require('lspconfig')[server_name].setup({})
    end,
  },
})
```

### Installing Formatters and Linters
You can install formatters and linters using Mason:
```
:MasonInstall black flake8 prettier eslint
```

## Setting Up Autoformatting
To configure autoformatting, install `conform.nvim`:

```lua
call('plug#begin', '~/.config/nvim/Plugged/')
Plug 'stevearc/conform.nvim'
call('plug#end')
```

Run:
```
:PlugInstall
```

Then, configure formatting in `init.lua`:
```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.py,*.js,*.ts,*.css,*.html",
  callback = function()
    vim.lsp.buf.format({ async = false })
  end,
})
```

## Checking Errors and LSP Status
To check LSP logs:
```
:LspInfo
```
To check installed Mason packages:
```
:Mason
```
To update Mason:
```
:MasonUpdate
```

## Useful Keybindings
```lua
vim.keymap.set("n", "gd", function() vim.lsp.buf.definition() end)
vim.keymap.set("n", "K", function() vim.lsp.buf.hover() end)
vim.keymap.set("n", "<leader>vca", function() vim.lsp.buf.code_action() end)
vim.keymap.set("n", "<F2>", function() vim.lsp.buf.rename() end)
```

## Additional Documentation
- [Mason.nvim](https://github.com/williamboman/mason.nvim)
- [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig)
- [Prettier](https://prettier.io/docs/en/install.html)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/)
- [ESLint](https://eslint.org/docs/latest/user-guide/getting-started)


