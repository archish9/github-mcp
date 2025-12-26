# GitHub MCP - Branch Management Examples

This directory contains examples for the Branch Management tools.

## Prerequisites

1. Install MCP Python SDK:
```bash
pip install mcp
```

2. Install GitHub MCP server:
```bash
pip install -e ../..
```

3. Set up GitHub token in `.env`:
```
GITHUB_TOKEN=your_github_personal_access_token
```

4. **For write operations** (create/delete/merge), add your repo:
```
GITHUB_REPO_OWNER=your-username
GITHUB_REPO_NAME=your-repo
```

---

## Available Scripts

### `individual_examples.py`

```bash
# Run all examples
python examples/branch_management/individual_examples.py

# Run specific example
python examples/branch_management/individual_examples.py list
python examples/branch_management/individual_examples.py protection
python examples/branch_management/individual_examples.py compare
python examples/branch_management/individual_examples.py create
python examples/branch_management/individual_examples.py delete
python examples/branch_management/individual_examples.py merge
```

### `interactive_demo.py`

```bash
python examples/branch_management/interactive_demo.py
```

---

## Available Tools

### 1. `list_branches`
List all branches in a repository.

```python
result = await session.call_tool(
    "list_branches",
    arguments={
        "owner": "facebook",
        "repo": "react",
        "protected_only": False  # Optional
    }
)
```

---

### 2. `create_branch`
Create a new branch. **Requires write access.**

```python
result = await session.call_tool(
    "create_branch",
    arguments={
        "owner": "your-username",
        "repo": "your-repo",
        "branch_name": "feature/new-feature",
        "from_branch": "main"  # Optional
    }
)
```

---

### 3. `delete_branch`
Delete a branch. **Requires write access.**

```python
result = await session.call_tool(
    "delete_branch",
    arguments={
        "owner": "your-username",
        "repo": "your-repo",
        "branch_name": "feature/old-feature"
    }
)
```

---

### 4. `merge_branches`
Merge one branch into another. **Requires write access.**

```python
result = await session.call_tool(
    "merge_branches",
    arguments={
        "owner": "your-username",
        "repo": "your-repo",
        "base": "main",
        "head": "feature/my-feature",
        "commit_message": "Merge feature"  # Optional
    }
)
```

---

### 5. `get_branch_protection`
Get branch protection rules.

```python
result = await session.call_tool(
    "get_branch_protection",
    arguments={
        "owner": "microsoft",
        "repo": "vscode",
        "branch": "main"  # Optional
    }
)
```

---

### 6. `compare_branches`
Compare two branches.

```python
result = await session.call_tool(
    "compare_branches",
    arguments={
        "owner": "facebook",
        "repo": "react",
        "base": "main",
        "head": "canary"
    }
)
```

---

## Troubleshooting

### Error: "Not Found" for branch operations
- Verify branch name exists
- Check repository permissions

### Error: "Forbidden" for create/delete/merge
- Ensure your token has write access (`repo` scope)
- These operations only work on repositories you own or have push access to
