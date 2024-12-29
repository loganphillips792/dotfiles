local wezterm = require("wezterm")

local function set_size_of_emulator()
 return {
  initial_rows = 20,
  initial_cols = 120,
  font_size = 15.0,
}
end

-- configuration file expects a table to be returned directly
return set_size_of_emulator()

