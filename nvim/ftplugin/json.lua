print("ftplugin/json.lua loaded")
vim.keymap.set("n", "<C-f>", ":%!jq .<CR>", { buffer = true, desc = "Format JSON with jq" })
