local wezterm = require("wezterm")

-- 1. Initialize the config builder
local config = wezterm.config_builder()

-- 2. Set global/simple properties directly
config.font = wezterm.font("MesloLGS Nerd Font Mono")
config.font_size = 15.0 -- Adjusted from 190 (which is massive!)
config.enable_tab_bar = true
-- config.window_background_opacity = 0.9
config.macos_window_background_blur = 10

config.colors = {
	foreground = "#CBE0F0",
	background = "#011423",
	cursor_bg = "#47FF9C",
	cursor_border = "#47FF9C",
	cursor_fg = "#011423",
	selection_bg = "#033259",
	selection_fg = "#CBE0F0",
	ansi = { "#214969", "#E52E2E", "#44FFB1", "#FFE073", "#0FC5ED", "#a277ff", "#24EAF7", "#24EAF7" },
	brights = { "#214969", "#E52E2E", "#44FFB1", "#FFE073", "#A277FF", "#a277ff", "#24EAF7", "#24EAF7" },
}

-- 3. Define helper functions that modify the config object directly
local function apply_size_settings(c)
  c.initial_rows = 20
  c.initial_cols = 120
end

local function apply_theme_settings(c)
  -- c.color_scheme = "Dracula (Official)"
  c.tab_bar_at_bottom = true
  c.use_fancy_tab_bar = false
  c.window_decorations = "RESIZE"
end

local function apply_background_settings(c)
  c.background = {
    -- Base layer: your solid background color
    {
      source = { Color = "#011423" },
      width = "100%",
      height = "100%",
    },
    -- Image layer on top, with reduced opacity so it doesn't wash out text
    {
      source = { File = '/Users/logan/dotfiles/wezterm-config/backgrounds/saturn-bg-wallpaper-background-removed.png' },
      hsb = { brightness = 0.3 },
      opacity = 0.3,
      horizontal_align = "Center",
      vertical_align = "Middle",
    },
  }
end

config.keys = {
  { key = "f", mods = "CMD|SHIFT", action = wezterm.action.ToggleFullScreen },
  { key = "k", mods = "CMD", action = wezterm.action.ClearScrollback("ScrollbackAndViewport") },
  { key = "!", mods = "CTRL|SHIFT", action = wezterm.action_callback(function(win, pane)
    local tab, window = pane:move_to_new_window()
  end) },
}

-- 4. Execute the functions to populate the config
apply_size_settings(config)
apply_theme_settings(config)
apply_background_settings(config)

-- 5. Return the config object
return config
