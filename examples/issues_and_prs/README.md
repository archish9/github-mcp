# GitHub MCP - Issues and PRs Examples

This directory contains demonstration scripts showing how to use the GitHub MCP server to create and manage issues and pull requests.

## Prerequisites

1. Install the MCP Python SDK:
```bash
pip install mcp
```

2. Make sure the GitHub MCP server is installed:
```bash
pip install -e ../..
```

3. **Configure your repository** - See [SETUP.md](SETUP.md) for detailed instructions.

   Quick setup: Add to `.env` file at project root:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPO_OWNER=your-username
   GITHUB_REPO_NAME=your-repo-name
   ```

4. **Important**: Your GitHub token needs the following permissions:
   - `repo` scope (for private repositories)
   - Or at least `public_repo` scope (for public repositories)

Get a token from: https://github.com/settings/tokens

> 📖 **New to this?** Check out [SETUP.md](SETUP.md) for a complete setup guide with troubleshooting!

## Available Demo Scripts

### 1. `demo_issues_and_prs.py` - Complete Demo
Runs through all issue and PR operations with interactive prompts.

**Usage:**
```bash
python examples/issues_and_prs/demo_issues_and_prs.py
```

**What it does:**
- Creates a new issue with labels
- Adds a comment to the issue
- Updates the issue (labels, body)
- Creates a pull request
- Adds a comment to the PR
- Updates the PR
- Demonstrates closing and reopening issues/PRs

**Note:** You'll be prompted to enter your repository details. Make sure you have write access to the repository.

---

### 2. `individual_examples.py` - Individual Tool Examples
Contains separate functions for each tool with multiple examples.

**Usage:**
```bash
# Run all examples
python examples/issues_and_prs/individual_examples.py

# Run specific example
python examples/issues_and_prs/individual_examples.py create_issue
python examples/issues_and_prs/individual_examples.py add_comment
python examples/issues_and_prs/individual_examples.py update_issue
python examples/issues_and_prs/individual_examples.py close_issue
python examples/issues_and_prs/individual_examples.py create_pr
python examples/issues_and_prs/individual_examples.py add_pr_comment
python examples/issues_and_prs/individual_examples.py update_pr
python examples/issues_and_prs/individual_examples.py close_pr
```

**Examples included:**
- **Create Issue**: Simple issue, issue with labels, issue with assignees
- **Add Comment**: Add comments to issues
- **Update Issue**: Update labels, assignees, title, body
- **Close/Reopen**: Close and reopen issues
- **Create PR**: Simple PR, draft PR, PR from fork
- **Add PR Comment**: Add comments to pull requests
- **Update PR**: Update title, body, base branch
- **Close/Reopen PR**: Close and reopen pull requests

**Note:** Before running, edit the script and replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name
- Issue/PR numbers with actual numbers from your repository

---

### 3. `interactive_demo.py` - Interactive Explorer
Interactive menu-driven demo where you can test with your own inputs.

**Usage:**
```bash
python examples/issues_and_prs/interactive_demo.py
```

**Features:**
- Menu-driven interface
- Enter your own parameters
- Formatted, readable output
- Error handling
- Test all operations interactively

**Example session:**
```
Select an option (0-10): 1
Owner (username/org): myusername
Repository name: myrepo
Issue title: Bug: Login button not working
Issue body (optional): The login button doesn't respond to clicks
Labels (comma-separated, optional): bug, urgent
Assignees (comma-separated usernames, optional): developer1
```

---

## Feature Examples

### Creating Issues

#### Simple Issue
```python
result = await session.call_tool(
    "create_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Bug: Login button not working",
        "body": "The login button on the homepage is not responding to clicks."
    }
)
```

#### Issue with Labels and Assignees
```python
result = await session.call_tool(
    "create_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Feature: Add dark mode",
        "body": "Implement a dark mode theme for the application.",
        "labels": ["enhancement", "ui", "feature-request"],
        "assignees": ["developer1", "developer2"]
    }
)
```

### Adding Comments

#### Comment on Issue
```python
result = await session.call_tool(
    "add_issue_comment",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1,
        "body": "I've investigated this issue and found the root cause."
    }
)
```

#### Comment on Pull Request
```python
result = await session.call_tool(
    "add_pr_comment",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 5,
        "body": "Great work! Just a few minor suggestions."
    }
)
```

### Updating Issues

#### Update Issue Labels
```python
result = await session.call_tool(
    "update_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1,
        "labels": ["bug", "high-priority", "urgent"]
    }
)
```

#### Update Issue Assignees
```python
result = await session.call_tool(
    "update_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1,
        "assignees": ["developer1", "developer2"]
    }
)
```

#### Update Issue Title and Body
```python
result = await session.call_tool(
    "update_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1,
        "title": "Updated: Bug fix for login button",
        "body": "This issue has been updated with more details."
    }
)
```

### Creating Pull Requests

#### Simple Pull Request
```python
result = await session.call_tool(
    "create_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Add user authentication",
        "body": "This PR adds user authentication functionality.",
        "head": "feature/auth",
        "base": "main"
    }
)
```

#### Draft Pull Request
```python
result = await session.call_tool(
    "create_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": "WIP: Add new feature",
        "body": "This is a work in progress. Do not merge yet.",
        "head": "feature/new-feature",
        "base": "main",
        "draft": True
    }
)
```

#### Pull Request from Fork
```python
result = await session.call_tool(
    "create_pull_request",
    arguments={
        "owner": "upstream-owner",
        "repo": "upstream-repo",
        "title": "Fix: Resolve bug in login",
        "body": "This PR fixes a bug in the login functionality.",
        "head": "fork-owner:fix-login-bug",  # Format: fork-owner:branch-name
        "base": "main"
    }
)
```

### Updating Pull Requests

#### Update PR Title and Body
```python
result = await session.call_tool(
    "update_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 1,
        "title": "Updated: Add user authentication with tests",
        "body": "This PR adds user authentication with comprehensive test coverage."
    }
)
```

#### Change PR Base Branch
```python
result = await session.call_tool(
    "update_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 1,
        "base": "develop"  # Change from main to develop
    }
)
```

### Closing and Reopening

#### Close Issue
```python
result = await session.call_tool(
    "close_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1
    }
)
```

#### Reopen Issue
```python
result = await session.call_tool(
    "reopen_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 1
    }
)
```

#### Close Pull Request
```python
result = await session.call_tool(
    "close_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 1
    }
)
```

#### Reopen Pull Request
```python
result = await session.call_tool(
    "reopen_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 1
    }
)
```

---

## Example Outputs

### Create Issue Response
```json
{
  "number": 42,
  "title": "Bug: Login button not working",
  "state": "open",
  "url": "https://github.com/myusername/myrepo/issues/42",
  "created_at": "2024-01-15T10:30:00Z",
  "labels": ["bug", "urgent"],
  "assignees": ["developer1"]
}
```

### Create Pull Request Response
```json
{
  "number": 15,
  "title": "Add user authentication",
  "state": "open",
  "url": "https://github.com/myusername/myrepo/pull/15",
  "created_at": "2024-01-15T10:30:00Z",
  "head": "feature/auth",
  "base": "main",
  "draft": false,
  "merged": false
}
```

### Add Comment Response
```json
{
  "id": 123456,
  "body": "I've investigated this issue and found the root cause.",
  "user": "myusername",
  "created_at": "2024-01-15T10:35:00Z",
  "url": "https://github.com/myusername/myrepo/issues/42#issuecomment-123456"
}
```

---

## Common Use Cases

### 1. Automated Bug Reporting
```python
# Create issue from error log
result = await session.call_tool(
    "create_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": f"Error: {error_type}",
        "body": f"Error occurred at {timestamp}\n\n```\n{traceback}\n```",
        "labels": ["bug", "auto-generated"]
    }
)
```

### 2. Bulk Issue Creation
```python
# Create multiple issues from a list
tasks = [
    {"title": "Task 1", "body": "Description 1"},
    {"title": "Task 2", "body": "Description 2"},
    {"title": "Task 3", "body": "Description 3"}
]

for task in tasks:
    result = await session.call_tool(
        "create_issue",
        arguments={
            "owner": "myusername",
            "repo": "myrepo",
            "title": task["title"],
            "body": task["body"],
            "labels": ["task"]
        }
    )
```

### 3. PR Creation from Feature Branch
```python
# Create PR after feature is complete
result = await session.call_tool(
    "create_pull_request",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Feature: Add user authentication",
        "body": "Implements user authentication with JWT tokens.",
        "head": "feature/auth",
        "base": "main"
    }
)
```

### 4. Issue Triage Workflow
```python
# Update issue with priority and assignee
result = await session.call_tool(
    "update_issue",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "issue_number": 42,
        "labels": ["bug", "high-priority"],
        "assignees": ["senior-developer"]
    }
)
```

### 5. PR Review Comments
```python
# Add review comment to PR
result = await session.call_tool(
    "add_pr_comment",
    arguments={
        "owner": "myusername",
        "repo": "myrepo",
        "pr_number": 15,
        "body": "Great work! Just a few suggestions:\n\n1. Add error handling\n2. Add unit tests"
    }
)
```

---

## Troubleshooting

### Error: "GITHUB_TOKEN environment variable is required"
**Solution:** Create a `.env` file at the project root with your GitHub token:
```bash
echo "GITHUB_TOKEN=your_token_here" > .env
```

### Error: "404 Not Found" when creating issue/PR
**Solution:** 
- Check that the repository exists and you have write access
- Verify the owner and repo names are correct
- Ensure your GitHub token has the `repo` scope

### Error: "Branch not found" when creating PR
**Solution:**
- Make sure the branch exists in the repository
- Check the branch name spelling
- For forks, use format: `fork-owner:branch-name`

### Error: "Label not found"
**Solution:**
- Labels must exist in the repository first
- Create labels in the repository settings before using them
- Check label names for typos

### Error: "Assignee not found"
**Solution:**
- Assignees must be collaborators on the repository
- Check username spelling
- Ensure the user has access to the repository

### Error: Rate limit exceeded
**Solution:** 
- GitHub API has rate limits (5000 requests/hour for authenticated users)
- Wait a few minutes before retrying
- Use an authenticated token for higher limits

---

## Best Practices

### 1. Error Handling
Always wrap tool calls in try-except blocks:
```python
try:
    result = await session.call_tool("create_issue", arguments={...})
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
```

### 2. Validate Inputs
Check that required fields are provided:
```python
if not owner or not repo or not title:
    print("Error: Missing required fields")
    return
```

### 3. Use Meaningful Titles
Create descriptive issue and PR titles:
```python
# Good
title = "Bug: Login button not responding on mobile devices"

# Bad
title = "Fix"
```

### 4. Provide Detailed Bodies
Include context and steps to reproduce:
```python
body = """
## Description
The login button doesn't respond to clicks on mobile devices.

## Steps to Reproduce
1. Open the app on mobile
2. Click the login button
3. Nothing happens

## Expected Behavior
The login form should appear.

## Environment
- Device: iPhone 12
- OS: iOS 15.0
- Browser: Safari
"""
```

### 5. Use Labels Effectively
Organize issues with consistent labels:
```python
labels = ["bug", "high-priority"]  # For bugs
labels = ["enhancement", "feature-request"]  # For features
labels = ["documentation"]  # For docs
```

---

## Creating Your Own Scripts

Basic template:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
load_dotenv(PROJECT_ROOT / ".env")

async def my_custom_script():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "github_mcp.server"],
        env=env,
        cwd=str(PROJECT_ROOT)
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Your custom tool calls here
            result = await session.call_tool(
                "create_issue",
                arguments={
                    "owner": "myusername",
                    "repo": "myrepo",
                    "title": "My Issue",
                    "body": "Issue description"
                }
            )
            
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(my_custom_script())
```

---

## Next Steps

1. Try the `interactive_demo.py` to explore the API interactively
2. Modify `individual_examples.py` with your own repositories
3. Create your own custom scripts based on your needs
4. Integrate the MCP server with Claude Desktop for AI-powered GitHub management!

---

## Additional Resources

- [GitHub Issues API](https://docs.github.com/en/rest/issues)
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls)
- [MCP Documentation](https://modelcontextprotocol.io)
- [PyGithub Documentation](https://pygithub.readthedocs.io)

