# General Cursor rules for MCP and integrations

The rules in this folder are **generic** for any project using Confluence/Jira and MCP. They do not mention specific projects, spaces, or page IDs.

## How to use

Copy files from `cursor-rules/` into your project’s **`.cursor/rules/`** folder:

- `mcp-integrations.mdc` — when the project uses MCP (mcp-atlassian), Confluence, and Jira.

After copying, Cursor will apply these rules in that project. Add your own rules if needed (e.g. space context or Epic → page mapping) in separate files under `.cursor/rules/`.
