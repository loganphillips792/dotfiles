-- Workaround for mason.nvim v2 breaking changes
-- Pin to v1.x until the ecosystem stabilizes
-- See: https://github.com/mason-org/mason.nvim/issues/1917
return {
  { "mason-org/mason.nvim", version = "^1.0.0" },
  { "mason-org/mason-lspconfig.nvim", version = "^1.0.0" },
}
