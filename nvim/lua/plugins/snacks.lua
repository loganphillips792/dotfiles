return {
  "folke/snacks.nvim",
  priority = 1000,
  lazy = false,
  init = function()
    -- Force-kill terminal buffers before quitting to prevent neovim from
    -- hanging on :q! while the dashboard asciiquarium process is still running.
    vim.api.nvim_create_autocmd("VimLeavePre", {
      callback = function()
        for _, buf in ipairs(vim.api.nvim_list_bufs()) do
          if vim.api.nvim_buf_is_valid(buf) and vim.bo[buf].buftype == "terminal" then
            pcall(vim.api.nvim_buf_delete, buf, { force = true })
          end
        end
      end,
    })
  end,
  ---@type snacks.Config
  opts = {
    dashboard = {
      enabled = true,
      sections = {
        { section = "header" },
        { section = "keys", gap = 1, padding = 1 },
        -- { section = "terminal", cmd = "asciiquarium -t", height = 10, width = 80, ttl = 0, padding = 1 },
        { section = "startup" },
      },
    },
    explorer = { enabled = true },
    image = { enabled = true },
    lazygit = {
      enabled = true,
      auto_close = false,
    },
    picker = {
      enabled = true,
      sources = {
        explorer = {
          hidden = true,
        },
      },
    },
  },
  keys = {
    { "<leader>e", function() Snacks.explorer() end, desc = "File Explorer" },
    { "<leader>/", function() Snacks.picker.grep() end, desc = "Grep" },
    { "<leader>:", function() Snacks.picker.command_history() end, desc = "Command History" },
    { "<leader>fr", function() Snacks.picker.recent() end, desc = "Recent" },
    { "<leader>l", function() Snacks.lazygit.open() end, desc = "Lazygit" },
  },
}
