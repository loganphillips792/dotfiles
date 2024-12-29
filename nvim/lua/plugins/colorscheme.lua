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

  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      vim.cmd([[colorscheme catppuccin-macchiato]])
    end
  }

}
