# GitHub MCP Server

A Model Context Protocol (MCP) server for GitHub integration.

## Features

- Search repositories
- Get repository information
- Read file contents
- List issues and pull requests
- Get user information

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Create a `.env` file with your GitHub token:
```
GITHUB_TOKEN=your_github_personal_access_token
```

3. Get a GitHub token from: https://github.com/settings/tokens

## Usage with Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["-m", "github_mcp.server"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Available Tools

- `search_repositories` - Search for repositories
- `get_repository_info` - Get repo details
- `get_file_contents` - Read file contents
- `list_issues` - List repository issues
- `list_pull_requests` - List pull requests
- `get_user_info` - Get user information

