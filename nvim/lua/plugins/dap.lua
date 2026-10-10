return {
  "mfussenegger/nvim-dap",
  event = "VeryLazy",
  dependencies = {
    { "rcarriga/nvim-dap-ui", dependencies = { "nvim-neotest/nvim-nio" } },
    -- installs codelldb via Mason and registers its adapter + default c/cpp/rust launch configs
    { "jay-babu/mason-nvim-dap.nvim", dependencies = { "mason-org/mason.nvim" } },
  },
  keys = {
    { "<leader>bb", "<cmd>DapToggleBreakpoint<CR>", desc = "Toggle breakpoint" },
    { "<leader>bc", "<cmd>DapContinue<CR>", desc = "Start/continue debugger" },
    { "<leader>bn", "<cmd>DapStepOver<CR>", desc = "Step over (next)" },
    { "<leader>bi", "<cmd>DapStepInto<CR>", desc = "Step into" },
    { "<leader>bo", "<cmd>DapStepOut<CR>", desc = "Step out" },
    { "<leader>bq", "<cmd>DapTerminate<CR>", desc = "Terminate debugger" },
    {
      "<leader>bu",
      function()
        require("dapui").toggle()
      end,
      desc = "Toggle debugger UI",
    },
  },
  config = function()
    local dap = require("dap")
    local dapui = require("dapui")

    require("mason-nvim-dap").setup({
      ensure_installed = { "codelldb" },
      handlers = {},
    })

    dapui.setup()

    -- open the UI when a session starts, close it when the program ends
    dap.listeners.after.event_initialized["dapui_config"] = function()
      dapui.open()
    end
    dap.listeners.before.event_terminated["dapui_config"] = function()
      dapui.close()
    end
    dap.listeners.before.event_exited["dapui_config"] = function()
      dapui.close()
    end
  end,
}
