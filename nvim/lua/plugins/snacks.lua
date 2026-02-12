return {
  "folke/snacks.nvim",
  priority = 1000,
  lazy = false,
  ---@type snacks.Config
  opts = {
    dashboard = { enabled = true },
    explorer = { enabled = true },
    image = { enabled = true },
    picker = { enabled = true },
  },
  keys = {
    { "<leader>e", function() Snacks.explorer() end, desc = "File Explorer" },
    { "<leader>/", function() Snacks.picker.grep() end, desc = "Grep" },
  },
}
