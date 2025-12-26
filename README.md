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

### Repository Statistics
- `get_contributor_stats` - Get contributor statistics (commits, additions, deletions per user)
- `get_code_frequency` - Get weekly additions/deletions over time
- `get_commit_activity` - Get commit activity by week for the past year
- `get_language_breakdown` - Get language breakdown by bytes
- `get_traffic_stats` - Get views, clones, popular paths (requires push access)
- `get_community_health` - Get community health metrics

### Commit History
- `list_commits` - Get list of commits with messages and authors
- `get_commit_details` - View specific commit details (files changed, diff)
- `search_commits` - Search commits by author, date, message
- `compare_commits` - Compare commits between branches/tags
- `get_commit_stats` - Get commit statistics for a time period

### Branch Management
- `list_branches` - List all branches in a repository
- `create_branch` - Create new branches
- `delete_branch` - Delete branches
- `merge_branches` - Merge one branch into another
- `get_branch_protection` - Get branch protection rules
- `compare_branches` - Compare two branches
