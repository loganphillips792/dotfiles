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

local function set_background_image()
  return {
    window_background_image = '/Users/logan/dotfiles/wezterm-config/backgrounds/image.jpg',
    window_background_image_hsb = {
      -- brightness = 0.3,
      hue = 1.0,
      saturdation = 1.0,
  },
}
end

-- General merge function to combine multiple tables
local function merge_tables(...)
  local merged = {}
  for _, tbl in ipairs({...}) do
    for k, v in pairs(tbl) do
      merged[k] = v
    end
  end
  return merged
end

-- configuration file expects a table to be returned directly
return merge_tables(set_size_of_emulator(), set_theme())

