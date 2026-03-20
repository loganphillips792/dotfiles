return {
  "lervag/vimtex",
  lazy = false,
  init = function()
    vim.g.vimtex_view_method = "skim" -- macOS PDF viewer with synctex
    vim.g.vimtex_compiler_method = "latexmk"
    vim.g.vimtex_quickfix_mode = 0

    -- Concealment: hide LaTeX markup for cleaner view
    vim.api.nvim_create_autocmd("FileType", {
      pattern = "tex",
      callback = function()
        vim.opt_local.conceallevel = 2
        vim.opt_local.spell = true
        vim.opt_local.spelllang = "en_us"
        vim.opt_local.wrap = true
        vim.opt_local.linebreak = true
        -- Ctrl+L in insert mode: fix previous spelling mistake without leaving flow
        vim.keymap.set("i", "<C-l>", "<c-g>u<Esc>[s1z=`]a<c-g>u", { buffer = true })
      end,
    })
  end,
}
