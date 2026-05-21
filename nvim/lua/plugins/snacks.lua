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

    -- When the explorer is already open, reveal the current file in it
    -- whenever a real file buffer is shown (e.g. opened from telescope).
    vim.api.nvim_create_autocmd("BufWinEnter", {
      callback = function(args)
        if not (_G.Snacks and Snacks.picker) then return end
        if Snacks.picker.get({ source = "explorer" })[1] == nil then return end
        if vim.bo[args.buf].buftype ~= "" then return end
        if vim.api.nvim_buf_get_name(args.buf) == "" then return end
        Snacks.explorer.reveal({ buf = args.buf })
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
    { "<leader>gB", function() Snacks.git.blame_line() end, desc = "Git Blame Line" },
  },
}
