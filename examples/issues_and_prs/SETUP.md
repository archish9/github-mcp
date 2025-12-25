# Setup Guide for Issues and PRs Examples

This guide will help you configure the examples to work with your GitHub repository.

## Quick Setup

### Option 1: Using Environment Variables (Recommended)

1. **Create or edit the `.env` file** in the project root (not in the examples folder):
   ```bash
   # In the project root: c:\laragon\www\AI-ML\github-mcp\.env
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPO_OWNER=your-username
   GITHUB_REPO_NAME=your-repo-name
   ```

2. **Get your GitHub token:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (for private repos) or `public_repo` (for public repos)
   - Copy the token and add it to `.env`

3. **Set your repository:**
   - `GITHUB_REPO_OWNER`: Your GitHub username or organization name
   - `GITHUB_REPO_NAME`: Your repository name

**Example `.env` file:**
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO_OWNER=octocat
GITHUB_REPO_NAME=Hello-World
```

### Option 2: Edit Scripts Directly

1. Open `individual_examples.py`
2. Find all instances of `"YOUR_USERNAME"` and replace with your username
3. Find all instances of `"YOUR_REPO"` and replace with your repo name

**Example:**
```python
# Before
"owner": "YOUR_USERNAME",
"repo": "YOUR_REPO",

# After
"owner": "octocat",
"repo": "Hello-World",
```

### Option 3: Use Interactive Demo

The `interactive_demo.py` script prompts you for values each time, so no configuration needed!

```bash
python examples/issues_and_prs/interactive_demo.py
```

## Verify Your Setup

### 1. Check Your GitHub Token

Make sure your token has the right permissions:
- For **public repositories**: `public_repo` scope
- For **private repositories**: `repo` scope
- For **organizations**: May need organization approval

### 2. Verify Repository Access

Make sure you have **write access** to the repository:
- For your own repositories: You should have write access by default
- For organization repositories: You need to be a collaborator with write permissions
- For forks: You can create issues/PRs in your fork

### 3. Test the Connection

Run a simple test:
```bash
python examples/issues_and_prs/interactive_demo.py
```

Select option 1 (Create Issue) and enter your repository details. If you get a 404 error, check:
- Repository name is correct
- You have access to the repository
- Token has correct permissions

## Common Issues

### Error: "Repository not found" (404)

**Causes:**
- Repository doesn't exist
- Repository name is misspelled
- You don't have access to the repository
- Token doesn't have the right permissions

**Solutions:**
1. Verify the repository exists: `https://github.com/OWNER/REPO`
2. Check spelling of owner and repo name
3. Ensure your token has `repo` or `public_repo` scope
4. For private repos, make sure your token has access

### Error: "Permission denied" (403)

**Causes:**
- Token doesn't have write permissions
- Repository is private and token doesn't have access
- Organization requires token approval

**Solutions:**
1. Regenerate token with `repo` scope
2. For organizations, get approval for the token
3. Check repository settings → Collaborators to ensure you have write access

### Error: "Label not found" (422)

**Causes:**
- Label doesn't exist in the repository
- Label name is misspelled

**Solutions:**
1. Create labels in repository settings first
2. Check existing labels: Repository → Issues → Labels
3. Use exact label names (case-sensitive)

### Error: "Issues disabled" or 422 error when creating issues

**Causes:**
- Issues feature is disabled in the repository
- Repository settings don't allow issue creation

**Solutions:**
1. Go to your repository on GitHub
2. Click **Settings** → **General** → Scroll to **Features**
3. Check the **Issues** checkbox to enable issues
4. Save changes
5. Try creating the issue again

### Error: Response shows "None" or empty error message

**Causes:**
- Network/connection issue
- Server error not properly formatted
- Token authentication issue

**Solutions:**
1. Run the test script to see detailed error:
   ```bash
   python examples/issues_and_prs/test_issue_creation.py
   ```
2. Check your `.env` file has `GITHUB_TOKEN` set correctly
3. Verify token hasn't expired: https://github.com/settings/tokens
4. Check network connection
5. Review the full error output from the test script

### Error: "Assignee not found" (422)

**Causes:**
- Username is incorrect
- User is not a collaborator on the repository

**Solutions:**
1. Verify username spelling
2. Ensure user is added as a collaborator
3. Check repository settings → Collaborators

## Repository Requirements

### For Creating Issues:
- ✅ Repository must exist
- ✅ You must have write access
- ✅ Token must have `repo` or `public_repo` scope

### For Creating Pull Requests:
- ✅ All issue requirements above
- ✅ You need a branch with changes
- ✅ Branch must exist in the repository

### For Labels:
- ✅ Labels must be created in repository settings first
- ✅ Go to: Repository → Issues → Labels → New label

### For Assignees:
- ✅ Users must be collaborators on the repository
- ✅ Add collaborators: Repository → Settings → Collaborators

## Testing Your Setup

### Step 1: Test Token
```bash
# Check if token is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', 'SET' if os.getenv('GITHUB_TOKEN') else 'NOT SET')"
```

### Step 2: Test Repository Access
```bash
# Use interactive demo to test
python examples/issues_and_prs/interactive_demo.py
# Select option 1, enter your repo details
```

### Step 3: Create a Test Issue
If everything works, you should see:
```json
{
  "number": 1,
  "title": "Bug: Login button not working",
  "state": "open",
  "url": "https://github.com/your-username/your-repo/issues/1"
}
```

## Next Steps

Once setup is complete:
1. Try `interactive_demo.py` to explore all features
2. Run `individual_examples.py` to see code examples
3. Run `demo_issues_and_prs.py` for a complete walkthrough
4. Create your own scripts using the examples as templates

## Getting Help

If you're still having issues:
1. Check the error message - it now includes helpful suggestions
2. Review the troubleshooting section in `README.md`
3. Verify your token permissions at https://github.com/settings/tokens
4. Check repository access at https://github.com/OWNER/REPO/settings/access

