"""
Interactive demo for Issues and PRs features
Menu-driven interface to test all features with your own inputs
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

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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

def print_menu():
    """Print the main menu"""
    print("\n" + "=" * 70)
    print("GitHub MCP - Issues and PRs Interactive Demo")
    print("=" * 70)
    print("\nIssue Operations:")
    print("  1. Create Issue")
    print("  2. Add Comment to Issue")
    print("  3. Update Issue")
    print("  4. Close Issue")
    print("  5. Reopen Issue")
    print("\nPull Request Operations:")
    print("  6. Create Pull Request")
    print("  7. Add Comment to PR")
    print("  8. Update Pull Request")
    print("  9. Close Pull Request")
    print(" 10. Reopen Pull Request")
    print("\n  0. Exit")
    print("=" * 70)

def print_result(result, title="Result"):
    """Pretty print JSON result"""
    print(f"\n{title}:")
    print("-" * 70)
    try:
        data = json.loads(result.content[0].text)
        print(json.dumps(data, indent=2))
    except:
        print(result.content[0].text)
    print()

async def create_issue(session):
    """Interactive: Create an issue"""
    print("\n--- Create Issue ---")
    owner = input("Owner (username/org): ").strip()
    repo = input("Repository name: ").strip()
    title = input("Issue title: ").strip()
    body = input("Issue body (optional, press Enter for empty): ").strip()
    labels_input = input("Labels (comma-separated, optional): ").strip()
    labels = [l.strip() for l in labels_input.split(",")] if labels_input else []
    assignees_input = input("Assignees (comma-separated usernames, optional): ").strip()
    assignees = [a.strip() for a in assignees_input.split(",")] if assignees_input else []
    
    try:
        result = await session.call_tool(
            "create_issue",
            arguments={
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body,
                "labels": labels,
                "assignees": assignees
            }
        )
        print_result(result, "✅ Issue Created")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def add_issue_comment(session):
    """Interactive: Add comment to issue"""
    print("\n--- Add Comment to Issue ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    issue_number = int(input("Issue number: ").strip())
    body = input("Comment body: ").strip()
    
    try:
        result = await session.call_tool(
            "add_issue_comment",
            arguments={
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
                "body": body
            }
        )
        print_result(result, "✅ Comment Added")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def update_issue(session):
    """Interactive: Update issue"""
    print("\n--- Update Issue ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    issue_number = int(input("Issue number: ").strip())
    
    print("\nWhat would you like to update? (leave blank to skip)")
    title = input("New title: ").strip() or None
    body = input("New body: ").strip() or None
    state = input("State (open/closed): ").strip() or None
    labels_input = input("Labels (comma-separated): ").strip()
    labels = [l.strip() for l in labels_input.split(",")] if labels_input else None
    assignees_input = input("Assignees (comma-separated): ").strip()
    assignees = [a.strip() for a in assignees_input.split(",")] if assignees_input else None
    
    args = {
        "owner": owner,
        "repo": repo,
        "issue_number": issue_number
    }
    if title:
        args["title"] = title
    if body:
        args["body"] = body
    if state:
        args["state"] = state
    if labels:
        args["labels"] = labels
    if assignees:
        args["assignees"] = assignees
    
    try:
        result = await session.call_tool("update_issue", arguments=args)
        print_result(result, "✅ Issue Updated")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def close_issue(session):
    """Interactive: Close issue"""
    print("\n--- Close Issue ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    issue_number = int(input("Issue number: ").strip())
    
    try:
        result = await session.call_tool(
            "close_issue",
            arguments={
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number
            }
        )
        print_result(result, "✅ Issue Closed")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def reopen_issue(session):
    """Interactive: Reopen issue"""
    print("\n--- Reopen Issue ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    issue_number = int(input("Issue number: ").strip())
    
    try:
        result = await session.call_tool(
            "reopen_issue",
            arguments={
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number
            }
        )
        print_result(result, "✅ Issue Reopened")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def create_pr(session):
    """Interactive: Create pull request"""
    print("\n--- Create Pull Request ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    title = input("PR title: ").strip()
    body = input("PR body (optional): ").strip()
    head = input("Head branch (branch with changes): ").strip()
    base = input("Base branch (target branch, default: main): ").strip() or "main"
    draft_input = input("Create as draft? (y/n, default: n): ").strip().lower()
    draft = draft_input == 'y'
    
    try:
        result = await session.call_tool(
            "create_pull_request",
            arguments={
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body,
                "head": head,
                "base": base,
                "draft": draft
            }
        )
        print_result(result, "✅ Pull Request Created")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def add_pr_comment(session):
    """Interactive: Add comment to PR"""
    print("\n--- Add Comment to Pull Request ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    pr_number = int(input("PR number: ").strip())
    body = input("Comment body: ").strip()
    
    try:
        result = await session.call_tool(
            "add_pr_comment",
            arguments={
                "owner": owner,
                "repo": repo,
                "pr_number": pr_number,
                "body": body
            }
        )
        print_result(result, "✅ Comment Added")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def update_pr(session):
    """Interactive: Update pull request"""
    print("\n--- Update Pull Request ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    pr_number = int(input("PR number: ").strip())
    
    print("\nWhat would you like to update? (leave blank to skip)")
    title = input("New title: ").strip() or None
    body = input("New body: ").strip() or None
    state = input("State (open/closed): ").strip() or None
    base = input("New base branch: ").strip() or None
    
    args = {
        "owner": owner,
        "repo": repo,
        "pr_number": pr_number
    }
    if title:
        args["title"] = title
    if body:
        args["body"] = body
    if state:
        args["state"] = state
    if base:
        args["base"] = base
    
    try:
        result = await session.call_tool("update_pull_request", arguments=args)
        print_result(result, "✅ Pull Request Updated")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def close_pr(session):
    """Interactive: Close pull request"""
    print("\n--- Close Pull Request ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    pr_number = int(input("PR number: ").strip())
    
    try:
        result = await session.call_tool(
            "close_pull_request",
            arguments={
                "owner": owner,
                "repo": repo,
                "pr_number": pr_number
            }
        )
        print_result(result, "✅ Pull Request Closed")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def reopen_pr(session):
    """Interactive: Reopen pull request"""
    print("\n--- Reopen Pull Request ---")
    owner = input("Owner: ").strip()
    repo = input("Repository: ").strip()
    pr_number = int(input("PR number: ").strip())
    
    try:
        result = await session.call_tool(
            "reopen_pull_request",
            arguments={
                "owner": owner,
                "repo": repo,
                "pr_number": pr_number
            }
        )
        print_result(result, "✅ Pull Request Reopened")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

async def main():
    """Main interactive loop"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n" + "=" * 70)
            print("Welcome to GitHub MCP Issues and PRs Interactive Demo!")
            print("=" * 70)
            print("\n⚠️  NOTE: You need write access to the repository to create/modify issues and PRs.")
            print("   Make sure you have a valid GITHUB_TOKEN with appropriate permissions.")
            
            while True:
                print_menu()
                choice = input("\nSelect an option (0-10): ").strip()
                
                if choice == "0":
                    print("\n👋 Goodbye!")
                    break
                elif choice == "1":
                    await create_issue(session)
                elif choice == "2":
                    await add_issue_comment(session)
                elif choice == "3":
                    await update_issue(session)
                elif choice == "4":
                    await close_issue(session)
                elif choice == "5":
                    await reopen_issue(session)
                elif choice == "6":
                    await create_pr(session)
                elif choice == "7":
                    await add_pr_comment(session)
                elif choice == "8":
                    await update_pr(session)
                elif choice == "9":
                    await close_pr(session)
                elif choice == "10":
                    await reopen_pr(session)
                else:
                    print("\n❌ Invalid option. Please try again.")
                
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())

