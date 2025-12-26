# GitHub MCP - Issues and Pull Requests Examples

Demonstration scripts for Issue and PR tools.

## Prerequisites

1. Install dependencies:
```bash
pip install mcp
pip install -e ../..
```

2. Configure `.env`:
```
GITHUB_TOKEN=your_github_token
```

3. **For write operations** (create/update/close):
```
GITHUB_REPO_OWNER=your-username
GITHUB_REPO_NAME=your-repo
```

---

## Scripts

### `individual_examples.py`

```bash
# List issues/PRs (read-only, works on any repo)
python examples/issues_and_prs/individual_examples.py list_issues
python examples/issues_and_prs/individual_examples.py list_prs

# Create/update (requires write access)
python examples/issues_and_prs/individual_examples.py create_issue
python examples/issues_and_prs/individual_examples.py create_pr

# Run all
python examples/issues_and_prs/individual_examples.py
```

### `interactive_demo.py`

```bash
python examples/issues_and_prs/interactive_demo.py
```

---

## Available Tools

### Issue Operations

| Tool | Description |
|------|-------------|
| `create_issue` | Create new issue with title, body, labels, assignees |
| `list_issues` | List issues with state/label filters |
| `add_issue_comment` | Add comment to an issue |
| `update_issue` | Update title, body, state, labels, assignees |
| `close_issue` | Close an issue |
| `reopen_issue` | Reopen a closed issue |

### Pull Request Operations

| Tool | Description |
|------|-------------|
| `create_pull_request` | Create PR from branches |
| `list_pull_requests` | List PRs with filters |
| `add_pr_comment` | Add comment to a PR |
| `update_pull_request` | Update PR details |
| `close_pull_request` | Close a PR |
| `reopen_pull_request` | Reopen a closed PR |

---

## Use Cases

### 1. Bulk Create Bug Reports
```python
bugs = [
    {"title": "Login fails on Safari", "labels": ["bug", "browser"]},
    {"title": "Memory leak in dashboard", "labels": ["bug", "performance"]},
]

for bug in bugs:
    await session.call_tool("create_issue", arguments={
        "owner": "myorg",
        "repo": "myapp",
        "title": bug["title"],
        "labels": bug["labels"]
    })
```

### 2. Close Stale Issues
```python
await session.call_tool("update_issue", arguments={
    "owner": "myorg",
    "repo": "myapp",
    "issue_number": 123,
    "state": "closed",
    "labels": ["wontfix"]
})
```

### 3. Create PR from Feature Branch
```python
await session.call_tool("create_pull_request", arguments={
    "owner": "myorg",
    "repo": "myapp",
    "title": "Add user authentication",
    "body": "Implements OAuth2 login",
    "head": "feature/auth",
    "base": "main"
})
```

---

## Troubleshooting

### "Not Found" error
- Check repository name and owner

### "Forbidden" for create/update
- Ensure your token has `repo` scope
- Verify you have write access
