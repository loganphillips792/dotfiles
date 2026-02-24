return {
  "mason-org/mason.nvim",
  dependencies = {
    "WhoIsSethDaniel/mason-tool-installer.nvim",
  },

  config = function()
    require("mason").setup({
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗",
        },
      },
    })

    require("mason-tool-installer").setup({
      ensure_installed = {
        -- LSP servers
        "html-lsp",
        "css-lsp",
        "tailwindcss-language-server",
        "lua-language-server",
        "graphql-language-service-cli",
        "gopls",
        "emmet-ls",
        "prisma-language-server",
        "pyright",
        "ruff",
        "templ",
        "vtsls",
        -- Formatters/linters (uncomment as needed)
        -- "prettier",
        -- "stylua",
        -- "isort",
        -- "black",
        -- "golines",
        -- "pylint",
        -- "eslint_d",
      },
    })
  end,
}
