return {
  "folke/which-key.nvim",
  event = "VeryLazy",
  opts = {
    preset = "classic",
    spec = {
      { "<leader>s", group = "search" },
      { "<leader>f", group = "file" },
      { "<leader>c", group = "code" },
      { "<leader>w", proxy = "<c-w>", group = "windows" },
    },
  },
  keys = {
    {
      "<leader>?",
      function()
        require("which-key").show({ global = false })
      end,
      desc = "Buffer Local Keymaps (which-key)",
    },
  },
}
