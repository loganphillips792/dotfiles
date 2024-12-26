return{
  {
      "nvim-neo-tree/neo-tree.nvim",
      branch = "v3.x",
      dependencies = {
        "nvim-lua/plenary.nvim",
        "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
        "MunifTanjim/nui.nvim",
        -- "3rd/image.nvim", -- Optional image support in preview window: See `# Preview Mode` for more information
      },
      config = function()
        -- Automatically open neo-tree on startup
	vim.cmd([[Neotree show]])

        require("neo-tree").setup({
		close_if_last_window = true,
          	enable_git_status=true,
        })
      end
  }
}
