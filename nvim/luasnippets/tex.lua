-- LaTeX snippets for LuaSnip (inspired by Gilles Castel's workflow)
local ls = require("luasnip")
local s = ls.snippet
local sn = ls.snippet_node
local t = ls.text_node
local i = ls.insert_node
local f = ls.function_node
local d = ls.dynamic_node
local fmta = require("luasnip.extras.fmt").fmta

-- Helper: check if cursor is in math zone (requires vimtex)
local function in_math()
  return vim.fn["vimtex#syntax#in_mathzone"]() == 1
end

local function not_in_math()
  return not in_math()
end

return {
  -- ── Environments ──────────────────────────────────────────────
  s({ trig = "beg", snippetType = "autosnippet", wordTrig = true }, fmta(
    [[
      \begin{<>}
          <>
      \end{<>}
    ]],
    { i(1), i(0), f(function(args) return args[1][1] end, { 1 }) }
  )),

  s("enum", fmta(
    [[
      \begin{enumerate}
          \item <>
      \end{enumerate}
    ]],
    { i(0) }
  )),

  s("item", fmta(
    [[
      \begin{itemize}
          \item <>
      \end{itemize}
    ]],
    { i(0) }
  )),

  s("desc", fmta(
    [[
      \begin{description}
          \item[<>] <>
      \end{description}
    ]],
    { i(1), i(0) }
  )),

  s("ali", fmta(
    [[
      \begin{align*}
          <>
      \end{align*}
    ]],
    { i(0) }
  )),

  -- ── Inline & display math ────────────────────────────────────
  s({ trig = "mk", snippetType = "autosnippet", wordTrig = true, condition = not_in_math },
    { t("$"), i(1), t("$") }
  ),

  s({ trig = "dm", snippetType = "autosnippet", wordTrig = true, condition = not_in_math }, fmta(
    [[
      \[
          <>
      .\]
    ]],
    { i(0) }
  )),

  -- ── Fractions ─────────────────────────────────────────────────
  s({ trig = "//", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\frac{<>}{<>}<>]],
    { i(1), i(2), i(0) }
  )),

  s({ trig = "(%d+)/", regTrig = true, snippetType = "autosnippet", condition = in_math },
    f(function(_, snip)
      return "\\frac{" .. snip.captures[1] .. "}"
    end),
    {}
  ),

  -- ── Sub & superscripts ────────────────────────────────────────
  s({ trig = "(%a)(%d)", regTrig = true, snippetType = "autosnippet", condition = in_math },
    f(function(_, snip)
      return snip.captures[1] .. "_" .. snip.captures[2]
    end)
  ),

  s({ trig = "(%a)_(%d%d)", regTrig = true, snippetType = "autosnippet", condition = in_math },
    f(function(_, snip)
      return snip.captures[1] .. "_{" .. snip.captures[2] .. "}"
    end)
  ),

  s({ trig = "sr", snippetType = "autosnippet", wordTrig = false, condition = in_math },
    t("^2")
  ),

  s({ trig = "cb", snippetType = "autosnippet", wordTrig = false, condition = in_math },
    t("^3")
  ),

  s({ trig = "compl", snippetType = "autosnippet", wordTrig = false, condition = in_math },
    t("^{c}")
  ),

  s({ trig = "td", snippetType = "autosnippet", wordTrig = false, condition = in_math }, fmta(
    [[^{<>}<>]],
    { i(1), i(0) }
  )),

  s({ trig = "__", snippetType = "autosnippet", wordTrig = false, condition = in_math }, fmta(
    [[_{<>}<>]],
    { i(1), i(0) }
  )),

  -- ── Greek letters ─────────────────────────────────────────────
  s({ trig = "@a", snippetType = "autosnippet", condition = in_math }, t("\\alpha")),
  s({ trig = "@b", snippetType = "autosnippet", condition = in_math }, t("\\beta")),
  s({ trig = "@g", snippetType = "autosnippet", condition = in_math }, t("\\gamma")),
  s({ trig = "@G", snippetType = "autosnippet", condition = in_math }, t("\\Gamma")),
  s({ trig = "@d", snippetType = "autosnippet", condition = in_math }, t("\\delta")),
  s({ trig = "@D", snippetType = "autosnippet", condition = in_math }, t("\\Delta")),
  s({ trig = "@e", snippetType = "autosnippet", condition = in_math }, t("\\epsilon")),
  s({ trig = "@ve", snippetType = "autosnippet", condition = in_math }, t("\\varepsilon")),
  s({ trig = "@z", snippetType = "autosnippet", condition = in_math }, t("\\zeta")),
  s({ trig = "@h", snippetType = "autosnippet", condition = in_math }, t("\\eta")),
  s({ trig = "@t", snippetType = "autosnippet", condition = in_math }, t("\\theta")),
  s({ trig = "@T", snippetType = "autosnippet", condition = in_math }, t("\\Theta")),
  s({ trig = "@k", snippetType = "autosnippet", condition = in_math }, t("\\kappa")),
  s({ trig = "@l", snippetType = "autosnippet", condition = in_math }, t("\\lambda")),
  s({ trig = "@L", snippetType = "autosnippet", condition = in_math }, t("\\Lambda")),
  s({ trig = "@m", snippetType = "autosnippet", condition = in_math }, t("\\mu")),
  s({ trig = "@n", snippetType = "autosnippet", condition = in_math }, t("\\nu")),
  s({ trig = "@x", snippetType = "autosnippet", condition = in_math }, t("\\xi")),
  s({ trig = "@p", snippetType = "autosnippet", condition = in_math }, t("\\pi")),
  s({ trig = "@P", snippetType = "autosnippet", condition = in_math }, t("\\Pi")),
  s({ trig = "@r", snippetType = "autosnippet", condition = in_math }, t("\\rho")),
  s({ trig = "@s", snippetType = "autosnippet", condition = in_math }, t("\\sigma")),
  s({ trig = "@S", snippetType = "autosnippet", condition = in_math }, t("\\Sigma")),
  s({ trig = "@u", snippetType = "autosnippet", condition = in_math }, t("\\tau")),
  s({ trig = "@f", snippetType = "autosnippet", condition = in_math }, t("\\phi")),
  s({ trig = "@vf", snippetType = "autosnippet", condition = in_math }, t("\\varphi")),
  s({ trig = "@c", snippetType = "autosnippet", condition = in_math }, t("\\chi")),
  s({ trig = "@ps", snippetType = "autosnippet", condition = in_math }, t("\\psi")),
  s({ trig = "@o", snippetType = "autosnippet", condition = in_math }, t("\\omega")),
  s({ trig = "@O", snippetType = "autosnippet", condition = in_math }, t("\\Omega")),

  -- ── Common operators & symbols ────────────────────────────────
  s({ trig = "->", snippetType = "autosnippet", priority = 100, condition = in_math }, t("\\to")),
  s({ trig = "!>", snippetType = "autosnippet", condition = in_math }, t("\\mapsto")),
  s({ trig = "=>", snippetType = "autosnippet", condition = in_math }, t("\\implies")),
  s({ trig = "=<", snippetType = "autosnippet", condition = in_math }, t("\\impliedby")),
  s({ trig = "iff", snippetType = "autosnippet", condition = in_math }, t("\\iff")),

  s({ trig = "<=", snippetType = "autosnippet", priority = 100, condition = in_math }, t("\\leq")),
  s({ trig = ">=", snippetType = "autosnippet", priority = 100, condition = in_math }, t("\\geq")),
  s({ trig = "!=", snippetType = "autosnippet", condition = in_math }, t("\\neq")),
  s({ trig = "~~", snippetType = "autosnippet", condition = in_math }, t("\\approx")),
  s({ trig = "~=", snippetType = "autosnippet", condition = in_math }, t("\\cong")),
  s({ trig = ">>", snippetType = "autosnippet", condition = in_math }, t("\\gg")),
  s({ trig = "<<", snippetType = "autosnippet", condition = in_math }, t("\\ll")),

  s({ trig = "xx", snippetType = "autosnippet", condition = in_math }, t("\\times")),
  s({ trig = "**", snippetType = "autosnippet", condition = in_math }, t("\\cdot")),
  s({ trig = "ooo", snippetType = "autosnippet", condition = in_math }, t("\\infty")),
  s({ trig = "...", snippetType = "autosnippet", condition = in_math }, t("\\ldots")),
  s({ trig = "+-", snippetType = "autosnippet", condition = in_math }, t("\\pm")),

  s({ trig = "cc", snippetType = "autosnippet", condition = in_math }, t("\\subset")),
  s({ trig = "cq", snippetType = "autosnippet", condition = in_math }, t("\\subseteq")),
  s({ trig = "notin", snippetType = "autosnippet", condition = in_math }, t("\\notin")),
  s({ trig = "inn", snippetType = "autosnippet", condition = in_math }, t("\\in")),
  s({ trig = "NN", snippetType = "autosnippet", condition = in_math }, t("\\mathbb{N}")),
  s({ trig = "ZZ", snippetType = "autosnippet", condition = in_math }, t("\\mathbb{Z}")),
  s({ trig = "QQ", snippetType = "autosnippet", condition = in_math }, t("\\mathbb{Q}")),
  s({ trig = "RR", snippetType = "autosnippet", condition = in_math }, t("\\mathbb{R}")),
  s({ trig = "CC", snippetType = "autosnippet", condition = in_math }, t("\\mathbb{C}")),
  s({ trig = "OO", snippetType = "autosnippet", condition = in_math }, t("\\emptyset")),
  s({ trig = "AA", snippetType = "autosnippet", condition = in_math }, t("\\forall")),
  s({ trig = "EE", snippetType = "autosnippet", condition = in_math }, t("\\exists")),

  -- ── Delimiters ────────────────────────────────────────────────
  s({ trig = "lr(", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\left( <> \right)<>]], { i(1), i(0) }
  )),

  s({ trig = "lr[", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\left[ <> \right]<>]], { i(1), i(0) }
  )),

  s({ trig = "lr{", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\left\{ <> \right\}<>]], { i(1), i(0) }
  )),

  s({ trig = "lr|", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\left| <> \right|<>]], { i(1), i(0) }
  )),

  s({ trig = "lra", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\left\langle <> \right\rangle<>]], { i(1), i(0) }
  )),

  -- ── Postfix: hat, bar, vec, tilde ─────────────────────────────
  s({ trig = "(%a)bar", regTrig = true, snippetType = "autosnippet", priority = 100, condition = in_math },
    f(function(_, snip) return "\\overline{" .. snip.captures[1] .. "}" end)
  ),
  s({ trig = "bar", condition = in_math, priority = 10 }, fmta(
    [[\overline{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "(%a)hat", regTrig = true, snippetType = "autosnippet", priority = 100, condition = in_math },
    f(function(_, snip) return "\\hat{" .. snip.captures[1] .. "}" end)
  ),
  s({ trig = "hat", condition = in_math, priority = 10 }, fmta(
    [[\hat{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "(%a)vec", regTrig = true, snippetType = "autosnippet", priority = 100, condition = in_math },
    f(function(_, snip) return "\\vec{" .. snip.captures[1] .. "}" end)
  ),
  s({ trig = "vec", condition = in_math, priority = 10 }, fmta(
    [[\vec{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "(%a)tld", regTrig = true, snippetType = "autosnippet", priority = 100, condition = in_math },
    f(function(_, snip) return "\\tilde{" .. snip.captures[1] .. "}" end)
  ),
  s({ trig = "tld", condition = in_math, priority = 10 }, fmta(
    [[\tilde{<>}<>]], { i(1), i(0) }
  )),

  -- ── Big operators ─────────────────────────────────────────────
  s({ trig = "sum", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\sum_{<> = <>}^{<>} <>]],
    { i(1, "n"), i(2, "1"), i(3, "\\infty"), i(0) }
  )),

  s({ trig = "prod", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\prod_{<> = <>}^{<>} <>]],
    { i(1, "n"), i(2, "1"), i(3, "\\infty"), i(0) }
  )),

  s({ trig = "lim", snippetType = "autosnippet", wordTrig = true, condition = in_math }, fmta(
    [[\lim_{<> \to <>} <>]],
    { i(1, "n"), i(2, "\\infty"), i(0) }
  )),

  s({ trig = "int", condition = in_math }, fmta(
    [[\int_{<>}^{<>} <> \, d<>]],
    { i(1, "-\\infty"), i(2, "\\infty"), i(3), i(0, "x") }
  )),

  s({ trig = "dint", condition = in_math }, fmta(
    [[\int_{<>}^{<>} <> \, d<>]],
    { i(1, "0"), i(2, "1"), i(3), i(0, "x") }
  )),

  -- ── Formatting ────────────────────────────────────────────────
  s({ trig = "tt", condition = in_math }, fmta(
    [[\text{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "bf", condition = in_math }, fmta(
    [[\mathbf{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "mcal", condition = in_math }, fmta(
    [[\mathcal{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "mbb", condition = in_math }, fmta(
    [[\mathbb{<>}<>]], { i(1), i(0) }
  )),

  s({ trig = "sq", snippetType = "autosnippet", condition = in_math }, fmta(
    [[\sqrt{<>}<>]], { i(1), i(0) }
  )),

  -- ── Document structure (non-math) ────────────────────────────
  s("sec", fmta([[\section{<>}<>]], { i(1), i(0) })),
  s("ssec", fmta([[\subsection{<>}<>]], { i(1), i(0) })),
  s("sssec", fmta([[\subsubsection{<>}<>]], { i(1), i(0) })),

  s("pac", fmta([[\usepackage{<>}<>]], { i(1), i(0) })),

  s("template", fmta(
    [[
      \documentclass[a4paper]{article}

      \usepackage[utf8]{inputenc}
      \usepackage[T1]{fontenc}
      \usepackage{amsmath, amssymb, amsthm}
      \usepackage{geometry}
      \usepackage{hyperref}

      \title{<>}
      \author{<>}
      \date{\today}

      \begin{document}
      \maketitle

      <>

      \end{document}
    ]],
    { i(1, "Title"), i(2, "Author"), i(0) }
  )),

  -- ── Theorem environments ──────────────────────────────────────
  s("thm", fmta(
    [[
      \begin{theorem}
          <>
      \end{theorem}
    ]],
    { i(0) }
  )),

  s("prf", fmta(
    [[
      \begin{proof}
          <>
      \end{proof}
    ]],
    { i(0) }
  )),

  s("def", fmta(
    [[
      \begin{definition}[<>]
          <>
      \end{definition}
    ]],
    { i(1), i(0) }
  )),

  s("lem", fmta(
    [[
      \begin{lemma}
          <>
      \end{lemma}
    ]],
    { i(0) }
  )),

  s("cor", fmta(
    [[
      \begin{corollary}
          <>
      \end{corollary}
    ]],
    { i(0) }
  )),

  -- ── Spell correction (Ctrl+L in insert mode) ─────────────────
  -- Configured in vimtex.lua via autocmd
}
