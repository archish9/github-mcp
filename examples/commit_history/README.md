# GitHub MCP - Commit History Examples

This directory contains demonstration scripts for the Commit History tools.

## Prerequisites

1. Install the MCP Python SDK:
```bash
pip install mcp
```

2. Install the GitHub MCP server:
```bash
pip install -e ../..
```

3. Set up your GitHub token in `.env` at the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
```

---

## Available Demo Scripts

### 1. `individual_examples.py` - Individual Tool Examples

**Usage:**
```bash
# Run all examples
python examples/commit_history/individual_examples.py

# Run specific example
python examples/commit_history/individual_examples.py list
python examples/commit_history/individual_examples.py details
python examples/commit_history/individual_examples.py search
python examples/commit_history/individual_examples.py compare
python examples/commit_history/individual_examples.py stats
```

### 2. `interactive_demo.py` - Interactive Explorer

```bash
python examples/commit_history/interactive_demo.py
```

---

## Available Tools

### 1. `list_commits`
Get list of commits with messages and authors.

```python
result = await session.call_tool(
    "list_commits",
    arguments={
        "owner": "microsoft",
        "repo": "vscode",
        "branch": "main",  # Optional
        "limit": 10  # Optional, default: 10
    }
)
```

---

### 2. `get_commit_details`
Get detailed information about a specific commit.

```python
result = await session.call_tool(
    "get_commit_details",
    arguments={
        "owner": "vercel",
        "repo": "next.js",
        "sha": "abc1234",  # Commit SHA
        "include_patch": True  # Optional, include diffs
    }
)
```

---

### 3. `search_commits`
Search commits by author, date, or file path.

```python
result = await session.call_tool(
    "search_commits",
    arguments={
        "owner": "python",
        "repo": "cpython",
        "author": "gvanrossum",  # Optional
        "since": "2024-01-01",  # Optional
        "until": "2024-12-31",  # Optional
        "path": "README.md",  # Optional
        "limit": 10
    }
)
```

---

### 4. `compare_commits`
Compare two commits, branches, or tags.

```python
result = await session.call_tool(
    "compare_commits",
    arguments={
        "owner": "facebook",
        "repo": "react",
        "base": "v18.0.0",  # Base branch/tag/commit
        "head": "main"  # Head branch/tag/commit
    }
)
```

---

### 5. `get_commit_stats`
Get commit statistics for a time period.

```python
result = await session.call_tool(
    "get_commit_stats",
    arguments={
        "owner": "vercel",
        "repo": "next.js",
        "days": 30  # Optional, default: 30
    }
)
```

---

## Example Outputs

### List Commits
```json
{
  "repository": "microsoft/vscode",
  "branch": "main",
  "total_returned": 5,
  "commits": [
    {
      "sha": "abc1234...",
      "short_sha": "abc1234",
      "message": "Fix bug in editor",
      "author": "John Doe",
      "date": "2024-01-15T10:30:00"
    }
  ]
}
```

### Compare Commits
```json
{
  "repository": "facebook/react",
  "base": "v18.0.0",
  "head": "main",
  "status": "ahead",
  "ahead_by": 150,
  "behind_by": 0,
  "total_commits": 150,
  "files_changed": 200
}
```

---

## Troubleshooting

### Error: "Commit not found"
- Verify the commit SHA is correct
- Use full SHA or at least 7 characters

### Error: "Branch not found"
- Check branch name spelling
- Use default branch if unsure

### Rate limit exceeded
- Wait a few minutes before retrying
- Use authenticated token for higher limits
