# GitHub MCP Server

A Model Context Protocol (MCP) server for GitHub integration.

## Features

- Search repositories
- Get repository information
- Read file contents
- List issues and pull requests
- Get user information
- **Create and manage issues** - Create issues, add comments, update status/labels/assignees
- **Create and manage pull requests** - Create PRs, add comments, update status

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

### Repository Operations
- `search_repositories` - Search for repositories
- `get_repository_info` - Get repo details
- `get_file_contents` - Read file contents
- `get_user_info` - Get user information

### Issue Operations
- `list_issues` - List repository issues
- `create_issue` - Create a new issue with title, body, labels, and assignees
- `add_issue_comment` - Add a comment to an issue
- `update_issue` - Update issue (title, body, state, labels, assignees, milestone)
- `close_issue` - Close an issue
- `reopen_issue` - Reopen a closed issue

### Pull Request Operations
- `list_pull_requests` - List pull requests
- `create_pull_request` - Create a new pull request from branches
- `add_pr_comment` - Add a comment to a pull request
- `update_pull_request` - Update PR (title, body, state, base branch)
- `close_pull_request` - Close a pull request
- `reopen_pull_request` - Reopen a closed pull request

