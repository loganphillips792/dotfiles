local opts = { noremap = true, silent = true }

local term_opts = { silent = true }

-- Shorten function name
local keymap = vim.api.nvim_set_keymap

--Remap space as leader key
keymap("", "<Space>", "<Nop>", opts)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Modes
--   normal_mode = "n",
--   insert_mode = "i",
--   visual_mode = "v",
--   visual_block_mode = "x",
--   term_mode = "t",
--   command_mode = "c",

-- Normal --
-- Better window navigation
keymap("n", "<C-h>", "<C-w>h", opts)
keymap("n", "<C-j>", "<C-w>j", opts)
keymap("n", "<C-k>", "<C-w>k", opts)
keymap("n", "<C-l>", "<C-w>l", opts)

keymap("n", "<leader>e", ":Lex 30<cr>", opts)

-- Jump to window by number
for i = 1, 9 do
    vim.keymap.set("n", "<Leader>" .. i, i .. "<C-w>w", { desc = "Move to Window " .. i })
end

-- Resize with arrows
keymap("n", "<C-Up>", ":resize +2<CR>", opts)
keymap("n", "<C-Down>", ":resize -2<CR>", opts)
keymap("n", "<C-Left>", ":vertical resize -2<CR>", opts)
keymap("n", "<C-Right>", ":vertical resize +2<CR>", opts)

-- Splits
vim.keymap.set("n", "<leader>|", "<cmd>vsplit<cr>", { desc = "Vertical Split" })
vim.keymap.set("n", "<leader>-", "<cmd>split<cr>", { desc = "Horizontal Split" })

-- Navigate buffers
keymap("n", "<S-l>", ":bnext<CR>", opts)
keymap("n", "<S-h>", ":bprevious<CR>", opts)

-- Insert --
-- Press jk fast to enter
keymap("i", "jk", "<ESC>", opts)

-- Visual --
-- Stay in indent mode
keymap("v", "<", "<gv", opts)
keymap("v", ">", ">gv", opts)

-- Move text up and down
keymap("v", "<A-j>", ":m .+1<CR>==", opts)
keymap("v", "<A-k>", ":m .-2<CR>==", opts)
keymap("v", "p", '"_dP', opts)

-- Visual Block --
-- Move text up and down
keymap("x", "J", ":move '>+1<CR>gv-gv", opts)
keymap("x", "K", ":move '<-2<CR>gv-gv", opts)
keymap("x", "<A-j>", ":move '>+1<CR>gv-gv", opts)
keymap("x", "<A-k>", ":move '<-2<CR>gv-gv", opts)

-- Smart window resize

-- Recursively walks the window layout tree to determine whether the
-- given window sits inside a "row" (side-by-side) or "col" (stacked) split.
local function find_parent_type(layout, winid)
    if layout[1] == "leaf" then return nil end
    for _, child in ipairs(layout[2]) do
        if child[1] == "leaf" and child[2] == winid then
            return layout[1]
        end
        local result = find_parent_type(child, winid)
        if result then return result end
    end
    return nil
end

-- Grows or shrinks the current window by 5 in the correct axis:
-- width for horizontal splits, height for vertical splits.
local function smart_resize(grow)
    local parent = find_parent_type(vim.fn.winlayout(), vim.api.nvim_get_current_win())
    local sign = grow and '+' or '-'
    if parent == "row" then
        vim.cmd('vertical resize ' .. sign .. '5')
    elseif parent == "col" then
        vim.cmd('resize ' .. sign .. '5')
    end
end
vim.keymap.set('n', '<leader>m', function() smart_resize(true) end, { desc = 'Expand Current Window' })
vim.keymap.set('n', '<leader>n', function() smart_resize(false) end, { desc = 'Shrink Current Window' })

-- Toggle wrap
vim.keymap.set('n', '<leader>w', function()
    vim.opt.wrap = not vim.opt.wrap:get()
    vim.opt.linebreak = vim.opt.wrap:get()
    print("Wrap: " .. (vim.opt.wrap:get() and "On" or "Off"))
end, { desc = 'Toggle Word Wrap and Linebreak' })

-- Terminal --
-- Better terminal navigation
keymap("t", "<C-h>", "<C-\\><C-N><C-w>h", term_opts)
keymap("t", "<C-j>", "<C-\\><C-N><C-w>j", term_opts)
keymap("t", "<C-k>", "<C-\\><C-N><C-w>k", term_opts)
keymap("t", "<C-l>", "<C-\\><C-N><C-w>l", term_opts)
