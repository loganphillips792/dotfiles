return {
  -- ... other plugins ...

  {
    "elihunter173/dirbuf.nvim",
    -- You can optionally set lazy = false if you always want it loaded immediately
    lazy = false,
    -- Use the `config` key if you want to do any extra configuration.
    config = function()
      -- Example: Create a convenient keybinding to open Dirbuf
      vim.keymap.set("n", "<leader>d", ":Dirbuf<CR>", { desc = "Open Dirbuf" })
    end,
  },

  -- ... more plugins ...
}
