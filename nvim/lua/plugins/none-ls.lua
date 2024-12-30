return {
  {
    "nvimtools/none-ls.nvim",
    ft = "go",
    opts = function()
      local null_ls = require("null-ls")
      local augroup = vim.api.nvim_create_augroup("LspFormatting", {})

      return {
        sources = {
          null_ls.builtins.formatting.gofumpt, -- go install mvdan.cc/gofumpt@latest
          null_ls.builtins.formatting.goimports_reviser, -- go install github.com/incu6us/goimports-reviser/v3@latest
          null_ls.builtins.formatting.golines, -- go install github.com/segmentio/golines@latest
        },
        on_attach = function(client, bufnr)
          if client.supports_method("textDocument/formatting") then
            vim.api.nvim_clear_autocmds({
              group = augroup,
              buffer = bufnr,
            })
            vim.api.nvim_create_autocmd("BufWritePre", {
              group = augroup,
              buffer = bufnr,
              callback = function()
                vim.lsp.buf.format({ bufnr = bufnr })
              end,
            })
          end
        end,
      }
    end,
  },
}
