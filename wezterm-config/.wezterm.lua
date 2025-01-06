local wezterm = require("wezterm")

local function set_size_of_emulator()
  return {
    initial_rows = 20,
    initial_cols = 120,
    font_size = 15.0,
  }
end

local function set_theme()  
  return {
      color_scheme = "Dracula (Official)",
      tab_bar_at_bottom = true,
      use_fancy_tab_bar = false,
      window_decorations = "RESIZE"
  }
end

-- Merge the two configurations
local function merge_tables(tbl1, tbl2)
  for k, v in pairs(tbl2) do
    tbl1[k] = v
  end
  return tbl1
end


-- configuration file expects a table to be returned directly
return merge_tables(set_size_of_emulator(), set_theme())

