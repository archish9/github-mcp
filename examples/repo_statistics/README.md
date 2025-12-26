# GitHub MCP - Repository Statistics Examples

This directory contains demonstration scripts showing how to use the GitHub MCP server's Repository Statistics tools.

## Prerequisites

1. Install the MCP Python SDK:
```bash
pip install mcp
```

2. Make sure the GitHub MCP server is installed:
```bash
pip install -e ../..
```

3. Set up your GitHub token in a `.env` file at the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
```

4. **For traffic statistics only**: Add your repository details:
```
GITHUB_REPO_OWNER=your-username
GITHUB_REPO_NAME=your-repo-name
```

> **Note:** Traffic statistics require push access to the repository. Other tools work with any public repository.

---

## Available Demo Scripts

### 1. `individual_examples.py` - Individual Tool Examples
Contains separate functions for each Repository Statistics tool.

**Usage:**
```bash
# Run all examples
python examples/repo_statistics/individual_examples.py

# Run specific example
python examples/repo_statistics/individual_examples.py contributors
python examples/repo_statistics/individual_examples.py code_frequency
python examples/repo_statistics/individual_examples.py commit_activity
python examples/repo_statistics/individual_examples.py languages
python examples/repo_statistics/individual_examples.py traffic
python examples/repo_statistics/individual_examples.py community
```

---

### 2. `interactive_demo.py` - Interactive Explorer
Interactive menu-driven demo where you can test with your own inputs.

**Usage:**
```bash
python examples/repo_statistics/interactive_demo.py
```

---

## Available Tools

### 1. `get_contributor_stats`
Get contributor statistics including commits, additions, and deletions per user.

```python
result = await session.call_tool(
    "get_contributor_stats",
    arguments={
        "owner": "python",
        "repo": "cpython",
        "limit": 10  # Optional, default: 10
    }
)
```

**Example Output:**
```json
{
  "repository": "python/cpython",
  "total_contributors": 2450,
  "showing": 10,
  "contributors": [
    {
      "author": "gvanrossum",
      "total_commits": 10456,
      "total_additions": 1234567,
      "total_deletions": 567890,
      "weeks_active": 520
    }
  ]
}
```

---

### 2. `get_code_frequency`
Get weekly additions and deletions over time.

```python
result = await session.call_tool(
    "get_code_frequency",
    arguments={
        "owner": "facebook",
        "repo": "react"
    }
)
```

**Example Output:**
```json
{
  "repository": "facebook/react",
  "total_additions": 2345678,
  "total_deletions": 1234567,
  "weeks_tracked": 520,
  "last_12_weeks": [
    {
      "week_start": "2024-01-07T00:00:00",
      "additions": 1234,
      "deletions": 567
    }
  ]
}
```

---

### 3. `get_commit_activity`
Get commit activity by week for the past year.

```python
result = await session.call_tool(
    "get_commit_activity",
    arguments={
        "owner": "microsoft",
        "repo": "vscode"
    }
)
```

**Example Output:**
```json
{
  "repository": "microsoft/vscode",
  "total_commits_year": 12345,
  "weeks_tracked": 52,
  "last_12_weeks": [
    {
      "week_start": "2024-01-07T00:00:00",
      "total_commits": 45,
      "days": [5, 8, 12, 10, 6, 3, 1]
    }
  ]
}
```

---

### 4. `get_language_breakdown`
Get language breakdown by bytes of code.

```python
result = await session.call_tool(
    "get_language_breakdown",
    arguments={
        "owner": "tensorflow",
        "repo": "tensorflow"
    }
)
```

**Example Output:**
```json
{
  "repository": "tensorflow/tensorflow",
  "total_bytes": 123456789,
  "languages": [
    {
      "language": "C++",
      "bytes": 45678901,
      "percentage": 37.0
    },
    {
      "language": "Python",
      "bytes": 34567890,
      "percentage": 28.0
    }
  ]
}
```

---

### 5. `get_traffic_stats`
Get traffic statistics including views, clones, and popular paths.

> **Note:** Requires push (write) access to the repository.

```python
result = await session.call_tool(
    "get_traffic_stats",
    arguments={
        "owner": "your-username",
        "repo": "your-repo"
    }
)
```

**Example Output:**
```json
{
  "repository": "your-username/your-repo",
  "views": {
    "total": 1234,
    "unique": 567
  },
  "clones": {
    "total": 89,
    "unique": 45
  },
  "top_paths": [
    {
      "path": "/readme",
      "title": "your-repo/README.md",
      "views": 234,
      "unique_visitors": 123
    }
  ],
  "top_referrers": [
    {
      "referrer": "google.com",
      "views": 100,
      "unique_visitors": 50
    }
  ]
}
```

---

### 6. `get_community_health`
Get community health metrics including code of conduct, contributing guide, etc.

```python
result = await session.call_tool(
    "get_community_health",
    arguments={
        "owner": "microsoft",
        "repo": "vscode"
    }
)
```

**Example Output:**
```json
{
  "repository": "microsoft/vscode",
  "health_percentage": 100,
  "description": "Visual Studio Code",
  "documentation": "https://code.visualstudio.com/docs",
  "files": {
    "code_of_conduct": "https://github.com/microsoft/vscode/blob/main/CODE_OF_CONDUCT.md",
    "contributing": "https://github.com/microsoft/vscode/blob/main/CONTRIBUTING.md",
    "issue_template": "https://github.com/microsoft/vscode/blob/main/.github/ISSUE_TEMPLATE.md",
    "license": "https://github.com/microsoft/vscode/blob/main/LICENSE.txt",
    "readme": "https://github.com/microsoft/vscode/blob/main/README.md"
  }
}
```

---

## Troubleshooting

### Error: "GITHUB_TOKEN environment variable is required"
**Solution:** Create a `.env` file with your GitHub token:
```bash
echo "GITHUB_TOKEN=your_token_here" > .env
```

### Error: "Statistics are being calculated by GitHub"
**Solution:** GitHub computes statistics asynchronously. Wait a few seconds and try again.

### Error: "Access denied" for traffic stats
**Solution:** Traffic statistics require push access. Use your own repository instead.

### Error: Rate limit exceeded
**Solution:** GitHub API has rate limits. Wait a few minutes or use an authenticated token for higher limits.

---

## Next Steps

1. Try the `interactive_demo.py` to explore the API interactively
2. Modify `individual_examples.py` with your own repositories
3. Integrate with Claude Desktop for AI-powered repository analysis!
