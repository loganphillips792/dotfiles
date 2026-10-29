# Global Agent Instructions

Harness-neutral instructions shared by every coding agent (Claude Code, Codex, opencode, pi).

## Jira
- I don't use the Atlassian Rovo MCP connector. Don't tell me you lack Jira access.
- To create, update, or search Jira tickets, call the Jira Cloud REST API (v3) directly with curl.
- Credentials are environment variables, defined in `~/.secrets.zsh` (not in the dotfiles repo; sourced by `~/.zshrc`):
  - `JIRA_EMAIL`: my Atlassian account email
  - `JIRA_API_TOKEN`: API token
  - `JIRA_BASE_URL`: e.g. `https://yourcompany.atlassian.net`
- If the variables are unset in your shell, run `source ~/.secrets.zsh` in the same command before calling curl.
- Auth: basic auth with `-u "$JIRA_EMAIL:$JIRA_API_TOKEN"`.
- Search with `GET/POST $JIRA_BASE_URL/rest/api/3/search/jql` (the old `/rest/api/3/search` is removed). Descriptions and comments use Atlassian Document Format (ADF) JSON.
- Never echo or print the token value.

## Knowledge base
- "My knowledge base" / "my KB" = my Obsidian vault at `/Volumes/NO_NAME/knowledge_base/` (external drive; if it's not mounted, say so instead of guessing).
- It's plain Markdown files. Read, search, and edit them directly with file tools.
- To look something up: search the vault (grep / glob) before answering.
- To update it: edit the relevant existing note if one fits; otherwise create a new note in the right folder. Use Obsidian `[[wikilinks]]` to link related notes.
- Keep my existing frontmatter and tags intact. Don't rename or move notes without asking.
- When adding new commands or keybinds to my tools, update the relevant knowledge base note.
