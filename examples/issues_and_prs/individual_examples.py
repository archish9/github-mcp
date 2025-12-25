"""
Individual examples for Issues and PRs features
Copy and modify these examples for your own use

SETUP INSTRUCTIONS:
===================

Before running these examples, you need to configure your repository:

Option 1 (Recommended): Set environment variables in .env file:
  GITHUB_REPO_OWNER=your-username
  GITHUB_REPO_NAME=your-repo-name

Option 2: Edit this file and replace 'YOUR_USERNAME' and 'YOUR_REPO' with your values

Option 3: Use interactive_demo.py which prompts for values

See SETUP.md for detailed instructions and troubleshooting.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# Build environment with PYTHONPATH
def get_server_env():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    return env

# Server configuration
SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "github_mcp.server"],
    env=get_server_env(),
    cwd=str(PROJECT_ROOT)
)

# Get default repository from environment or config
def get_default_repo():
    """Get default repository from environment variables or return None"""
    owner = os.getenv("GITHUB_REPO_OWNER")
    repo = os.getenv("GITHUB_REPO_NAME")
    return (owner, repo) if owner and repo else (None, None)

def validate_repo(owner, repo, operation="operation"):
    """Validate repository parameters and provide helpful error messages"""
    if not owner or owner == "YOUR_USERNAME":
        print("\n" + "=" * 70)
        print("ERROR: Invalid Repository Owner")
        print("=" * 70)
        print("\nYou need to set the repository owner (username or organization).")
        print("\nOptions:")
        print("1. Set environment variables in .env file:")
        print("   GITHUB_REPO_OWNER=your-username")
        print("   GITHUB_REPO_NAME=your-repo-name")
        print("\n2. Edit this script and replace 'YOUR_USERNAME' with your actual username")
        print("3. Use the interactive_demo.py which prompts for values")
        print("\nExample:")
        print("   owner='octocat'  # Your GitHub username")
        print("   repo='Hello-World'  # Your repository name")
        return False
    
    if not repo or repo == "YOUR_REPO":
        print("\n" + "=" * 70)
        print("ERROR: Invalid Repository Name")
        print("=" * 70)
        print("\nYou need to set the repository name.")
        print("\nOptions:")
        print("1. Set environment variables in .env file:")
        print("   GITHUB_REPO_OWNER=your-username")
        print("   GITHUB_REPO_NAME=your-repo-name")
        print("\n2. Edit this script and replace 'YOUR_REPO' with your actual repo name")
        print("3. Use the interactive_demo.py which prompts for values")
        return False
    
    return True

def print_result(result, title="Result"):
    """Pretty print JSON result with error handling"""
    print(f"\n{title}:")
    print("-" * 70)
    try:
        text = result.content[0].text
        data = json.loads(text)
        
        # Check for error responses
        if isinstance(data, dict) and "error" in data:
            print("ERROR:")
            error_msg = data.get('message') or data.get('error') or 'Unknown error'
            print(f"   {error_msg}")
            
            if "hint" in data:
                print(f"\nHint: {data['hint']}")
            
            if "suggestions" in data:
                print("\nSuggestions:")
                for suggestion in data["suggestions"]:
                    print(f"   - {suggestion}")
            
            # Print full error details for debugging
            if "details" in data:
                print(f"\nDetails: {data['details']}")
            
            # Print status code if available
            if "status" in data:
                print(f"\nStatus Code: {data['status']}")
        else:
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        # If not JSON, print as-is
        text = result.content[0].text
        print("ERROR (Non-JSON response):")
        print(text)
        print("\nThis might be a connection or server error.")
    except Exception as e:
        print(f"Error parsing result: {e}")
        print(f"\nRaw response:")
        print(result.content[0].text)
    print()

async def example_create_issue():
    """Example: Create a new issue"""
    # Get default repo from environment or use placeholders
    default_owner, default_repo = get_default_repo()
    owner = default_owner or "YOUR_USERNAME"
    repo = default_repo or "YOUR_REPO"
    
    # Validate repository info
    if not validate_repo(owner, repo, "create issue"):
        return
    
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Create Issue")
            print("=" * 70)
            print(f"\nRepository: {owner}/{repo}")
            print("Note: Make sure you have write access to this repository!")
            print()
            
            # Example 1: Simple issue
            print("\n1. Creating a simple issue...")
            try:
                result = await session.call_tool(
                    "create_issue",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": "Bug: Login button not working",
                        "body": "The login button on the homepage is not responding to clicks."
                    }
                )
                # Debug: Check if result has content
                if not result or not result.content:
                    print("ERROR: Empty response from server")
                    return
                print_result(result, "Created Issue")
            except Exception as e:
                print(f"Exception occurred: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
            
            # Example 2: Issue with labels
            print("\n2. Creating issue with labels...")
            print("   Note: Labels must exist in the repository first!")
            try:
                result = await session.call_tool(
                    "create_issue",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": "Feature: Add dark mode",
                        "body": "Implement a dark mode theme for the application.",
                        "labels": ["enhancement", "ui", "feature-request"]
                    }
                )
                print_result(result, "Created Issue with Labels")
            except Exception as e:
                print(f"Exception: {e}")
            
            # Example 3: Issue with assignees
            print("\n3. Creating issue with assignees...")
            print("   Note: Assignees must be collaborators on the repository!")
            try:
                result = await session.call_tool(
                    "create_issue",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": "Task: Update documentation",
                        "body": "Update the README with new installation instructions.",
                        "labels": ["documentation", "task"],
                        "assignees": []  # Empty list - add usernames if you have collaborators
                    }
                )
                print_result(result, "Created Issue with Assignees")
            except Exception as e:
                print(f"Exception: {e}")

async def example_add_issue_comment():
    """Example: Add comment to an issue"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Add Issue Comment")
            print("=" * 70)
            
            result = await session.call_tool(
                "add_issue_comment",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": 1,  # Replace with actual issue number
                    "body": "I've investigated this issue and found the root cause. Working on a fix now."
                }
            )
            print_result(result, "Added Comment")

async def example_update_issue():
    """Example: Update an issue"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Update Issue")
            print("=" * 70)
            
            # Example 1: Update labels
            print("\n1. Updating issue labels...")
            result = await session.call_tool(
                "update_issue",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": 1,
                    "labels": ["bug", "high-priority", "urgent"]
                }
            )
            print_result(result, "Updated Issue Labels")
            
            # Example 2: Update assignees
            print("\n2. Updating issue assignees...")
            result = await session.call_tool(
                "update_issue",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": 1,
                    "assignees": ["developer1", "developer2"]
                }
            )
            print_result(result, "Updated Issue Assignees")
            
            # Example 3: Update title and body
            print("\n3. Updating issue title and body...")
            result = await session.call_tool(
                "update_issue",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": 1,
                    "title": "Updated: Bug fix for login button",
                    "body": "This issue has been updated with more details.\n\n**Status:** In progress\n**ETA:** Next release"
                }
            )
            print_result(result, "Updated Issue Content")

async def example_close_reopen_issue():
    """Example: Close and reopen an issue"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Close and Reopen Issue")
            print("=" * 70)
            
            issue_number = 1  # Replace with actual issue number
            
            # Close issue
            print("\n1. Closing issue...")
            result = await session.call_tool(
                "close_issue",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": issue_number
                }
            )
            print_result(result, "Closed Issue")
            
            # Reopen issue
            print("\n2. Reopening issue...")
            result = await session.call_tool(
                "reopen_issue",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "issue_number": issue_number
                }
            )
            print_result(result, "Reopened Issue")

async def example_create_pull_request():
    """Example: Create a pull request"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Create Pull Request")
            print("=" * 70)
            
            # Example 1: Simple PR
            print("\n1. Creating a simple pull request...")
            result = await session.call_tool(
                "create_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "title": "Add user authentication",
                    "body": "This PR adds user authentication functionality.",
                    "head": "feature/auth",
                    "base": "main"
                }
            )
            print_result(result, "Created Pull Request")
            
            # Example 2: Draft PR
            print("\n2. Creating a draft pull request...")
            result = await session.call_tool(
                "create_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "title": "WIP: Add new feature",
                    "body": "This is a work in progress. Do not merge yet.",
                    "head": "feature/new-feature",
                    "base": "main",
                    "draft": True
                }
            )
            print_result(result, "Created Draft Pull Request")
            
            # Example 3: PR from fork
            print("\n3. Creating PR from a fork...")
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
            print_result(result, "Created PR from Fork")

async def example_add_pr_comment():
    """Example: Add comment to a pull request"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Add PR Comment")
            print("=" * 70)
            
            result = await session.call_tool(
                "add_pr_comment",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "pr_number": 1,  # Replace with actual PR number
                    "body": "Great work! Just a few minor suggestions:\n\n1. Consider adding error handling\n2. Add unit tests for this feature"
                }
            )
            print_result(result, "Added PR Comment")

async def example_update_pull_request():
    """Example: Update a pull request"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Update Pull Request")
            print("=" * 70)
            
            # Example 1: Update title and body
            print("\n1. Updating PR title and body...")
            result = await session.call_tool(
                "update_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "pr_number": 1,
                    "title": "Updated: Add user authentication with tests",
                    "body": "This PR adds user authentication with comprehensive test coverage.\n\n**Changes:**\n- Added login functionality\n- Added unit tests\n- Updated documentation"
                }
            )
            print_result(result, "Updated PR")
            
            # Example 2: Change base branch
            print("\n2. Changing PR base branch...")
            result = await session.call_tool(
                "update_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "pr_number": 1,
                    "base": "develop"  # Change from main to develop
                }
            )
            print_result(result, "Updated PR Base Branch")

async def example_close_reopen_pr():
    """Example: Close and reopen a pull request"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("Example: Close and Reopen Pull Request")
            print("=" * 70)
            
            pr_number = 1  # Replace with actual PR number
            
            # Close PR
            print("\n1. Closing pull request...")
            result = await session.call_tool(
                "close_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "pr_number": pr_number
                }
            )
            print_result(result, "Closed Pull Request")
            
            # Reopen PR
            print("\n2. Reopening pull request...")
            result = await session.call_tool(
                "reopen_pull_request",
                arguments={
                    "owner": "YOUR_USERNAME",
                    "repo": "YOUR_REPO",
                    "pr_number": pr_number
                }
            )
            print_result(result, "Reopened Pull Request")

# Main function to run examples
async def main():
    """Run all examples or specific example based on command line argument"""
    import sys
    
    examples = {
        "create_issue": example_create_issue,
        "add_comment": example_add_issue_comment,
        "update_issue": example_update_issue,
        "close_issue": example_close_reopen_issue,
        "create_pr": example_create_pull_request,
        "add_pr_comment": example_add_pr_comment,
        "update_pr": example_update_pull_request,
        "close_pr": example_close_reopen_pr,
    }
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        if example_name in examples:
            await examples[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        print("Running all examples...")
        print("(Note: Replace YOUR_USERNAME, YOUR_REPO, and issue/PR numbers with actual values)")
        print()
        for name, func in examples.items():
            try:
                await func()
                print("\n" + "=" * 70 + "\n")
            except Exception as e:
                print(f"Error in {name}: {e}")
                print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

