return {
  --[=[{
  "folke/tokyonight.nvim",
    lazy = false,
    priority=1000,
    opts = { style = "moon" },
    config = function()
      vim.cmd([[colorscheme tokyonight]])
    end
  } --]=]

  --[=[
  {
    "franbach/miramare",
    config = function()
      vim.cmd([[colorscheme miramare]])
    end
  }
  --]=]

   --[=[{
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      vim.cmd([[colorscheme catppuccin-macchiato]])
    end
  }
  --]=]
  
  "sainnhe/gruvbox-material",
  priority = 1000,
  config = function()
    vim.o.background = "dark" -- or "light" for light mode
    vim.cmd("let g:gruvbox_material_background= 'hard'")
    vim.cmd("let g:gruvbox_material_transparent_background=2")
    vim.cmd("let g:gruvbox_material_diagnostic_line_highlight=1")
    vim.cmd("let g:gruvbox_material_diagnostic_virtual_text='colored'")
    vim.cmd("let g:gruvbox_material_enable_bold=1")
    vim.cmd("let g:gruvbox_material_enable_italic=1")
    vim.cmd([[colorscheme gruvbox-material]]) -- Set color scheme
    -- changing bg and border colors
    vim.api.nvim_set_hl(0, "FloatBorder", { link = "Normal" })
    vim.api.nvim_set_hl(0, "LspInfoBorder", { link = "Normal" })
    vim.api.nvim_set_hl(0, "NormalFloat", { link = "Normal" })
    vim.api.nvim_set_hl(0, "Pmenu", { link = "Normal" })
    vim.api.nvim_set_hl(0, "PmenuSel", { link = "Search" })
    vim.api.nvim_set_hl(0, "BlinkCmpMenu", { link = "Normal" })
    vim.api.nvim_set_hl(0, "BlinkCmpMenuBorder", { link = "Normal" })
    vim.api.nvim_set_hl(0, "BlinkCmpMenuSelection", { link = "Search" })
    vim.api.nvim_set_hl(0, "BlinkCmpLabelMatch", { link = "Search" })
  end,
}
