return {
  'MagicDuck/grug-far.nvim',
  config = function()
    require('grug-far').setup({})
  end,
  keys = {
    { '<leader>r', '<cmd>GrugFar<cr>', desc = 'Search and Replace' },
    { '<leader>R', '<cmd>lua require("grug-far").open({ prefills = { search = vim.fn.expand("<cword>") } })<cr>', desc = 'Replace Current Word' },
    { '<leader>r', '<cmd>lua require("grug-far").with_visual_selection()<cr>', mode = 'v', desc = 'Replace Visual Selection' },
  },
}
