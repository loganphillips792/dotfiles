return {
  "nvimdev/dashboard-nvim",
  event = "VimEnter",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  config = function()
    require("dashboard").setup({
      theme = "hyper",
      config = {
        week_header = {
          enable = true,
        },
        shortcut = {
          { desc = " Find File", group = "DashboardShortCut", key = "f", action = "Telescope find_files" },
          { desc = " Recent Files", group = "DashboardShortCut", key = "r", action = "Telescope oldfiles" },
          { desc = " Find Word", group = "DashboardShortCut", key = "g", action = "Telescope live_grep" },
          { desc = " Config", group = "DashboardShortCut", key = "c", action = "e ~/.config/nvim/init.lua" },
          { desc = " Quit", group = "DashboardShortCut", key = "q", action = "qa" },
        },
        packages = { enable = true },
        project = { enable = true, limit = 5, action = "Telescope find_files cwd=" },
        mru = { enable = true, limit = 5 },
        footer = {},
      },
    })
  end,
}
