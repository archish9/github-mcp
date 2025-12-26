"""
Individual examples for Issues and Pull Requests tools

Run a specific example:
    python examples/issues_and_prs/individual_examples.py list_issues
    python examples/issues_and_prs/individual_examples.py list_prs
    python examples/issues_and_prs/individual_examples.py create_issue
    python examples/issues_and_prs/individual_examples.py create_pr
    python examples/issues_and_prs/individual_examples.py comment
    python examples/issues_and_prs/individual_examples.py update

Run all examples:
    python examples/issues_and_prs/individual_examples.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
load_dotenv(PROJECT_ROOT / ".env")

def get_server_env():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    return env

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "github_mcp.server"],
    env=get_server_env(),
    cwd=str(PROJECT_ROOT)
)

def print_result(result, title="Result"):
    """Pretty print JSON result"""
    print(f"\n{title}:")
    print("-" * 70)
    try:
        text = result.content[0].text
        data = json.loads(text)
        if isinstance(data, dict) and "error" in data:
            print("ERROR:")
            print(f"   {data.get('message', data.get('error'))}")
        else:
            print(json.dumps(data, indent=2))
    except:
        print(result.content[0].text)
    print()


async def example_list_issues():
    """Example: List issues from a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: List Issues")
                print("=" * 70)
                
                # List open issues
                print("\n1. Listing open issues from facebook/react...")
                result = await session.call_tool(
                    "list_issues",
                    arguments={
                        "owner": "facebook",
                        "repo": "react",
                        "state": "open",
                        "limit": 5
                    }
                )
                print_result(result, "Open Issues")
                
                # List issues with specific labels
                print("\n2. Listing bug issues from vercel/next.js...")
                result = await session.call_tool(
                    "list_issues",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js",
                        "state": "open",
                        "labels": "bug",
                        "limit": 5
                    }
                )
                print_result(result, "Bug Issues")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_list_prs():
    """Example: List pull requests from a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: List Pull Requests")
                print("=" * 70)
                
                # List open PRs
                print("\n1. Listing open PRs from microsoft/vscode...")
                result = await session.call_tool(
                    "list_pull_requests",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "state": "open",
                        "limit": 5
                    }
                )
                print_result(result, "Open PRs")
                
                # List recently merged PRs
                print("\n2. Listing closed PRs from facebook/react...")
                result = await session.call_tool(
                    "list_pull_requests",
                    arguments={
                        "owner": "facebook",
                        "repo": "react",
                        "state": "closed",
                        "limit": 5
                    }
                )
                print_result(result, "Closed PRs")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_create_issue():
    """Example: Create a new issue (requires write access)"""
    owner = os.getenv("GITHUB_REPO_OWNER")
    repo = os.getenv("GITHUB_REPO_NAME")
    
    if not owner or not repo:
        print("=" * 70)
        print("Example: Create Issue")
        print("=" * 70)
        print("\nNote: This example requires write access to a repository.")
        print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file.")
        print("\nExample usage (in code):")
        print('  await session.call_tool("create_issue", arguments={')
        print('      "owner": "your-username",')
        print('      "repo": "your-repo",')
        print('      "title": "Bug: Application crashes on startup",')
        print('      "body": "## Description\\nThe app crashes when...",')
        print('      "labels": ["bug", "priority:high"],')
        print('      "assignees": ["developer1"]')
        print("  })")
        return
    
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Create Issue")
                print("=" * 70)
                
                import time
                issue_title = f"Test Issue - {int(time.time())}"
                
                print(f"\nCreating issue in {owner}/{repo}...")
                result = await session.call_tool(
                    "create_issue",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": issue_title,
                        "body": "## Description\nThis is a test issue created via MCP.\n\n## Steps to reproduce\n1. Step one\n2. Step two\n\n## Expected behavior\nThe expected behavior."
                    }
                )
                print_result(result, "Created Issue")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_create_pr():
    """Example: Create a pull request (requires write access)"""
    print("=" * 70)
    print("Example: Create Pull Request")
    print("=" * 70)
    print("\nNote: This requires write access and existing branches.")
    print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file.")
    print("\nExample usage (in code):")
    print('  await session.call_tool("create_pull_request", arguments={')
    print('      "owner": "your-username",')
    print('      "repo": "your-repo",')
    print('      "title": "Add new feature",')
    print('      "body": "This PR adds...",')
    print('      "head": "feature/my-feature",')
    print('      "base": "main"')
    print("  })")


async def example_comment():
    """Example: Add comments to issues/PRs"""
    print("=" * 70)
    print("Example: Add Comments")
    print("=" * 70)
    print("\nFor Issues:")
    print('  await session.call_tool("add_issue_comment", arguments={')
    print('      "owner": "owner",')
    print('      "repo": "repo",')
    print('      "issue_number": 123,')
    print('      "body": "Thanks for reporting this!"')
    print("  })")
    print("\nFor Pull Requests:")
    print('  await session.call_tool("add_pr_comment", arguments={')
    print('      "owner": "owner",')
    print('      "repo": "repo",')
    print('      "pr_number": 456,')
    print('      "body": "LGTM!"')
    print("  })")


async def example_update():
    """Example: Update issues/PRs"""
    print("=" * 70)
    print("Example: Update Issue/PR")
    print("=" * 70)
    print("\nUpdate Issue:")
    print('  await session.call_tool("update_issue", arguments={')
    print('      "owner": "owner",')
    print('      "repo": "repo",')
    print('      "issue_number": 123,')
    print('      "labels": ["bug", "priority:high"],')
    print('      "assignees": ["developer1"],')
    print('      "state": "closed"')
    print("  })")
    print("\nClose/Reopen:")
    print('  await session.call_tool("close_issue", arguments={...})')
    print('  await session.call_tool("reopen_issue", arguments={...})')
    print('  await session.call_tool("close_pull_request", arguments={...})')
    print('  await session.call_tool("reopen_pull_request", arguments={...})')


async def run_all_examples():
    """Run all examples"""
    examples = [
        ("List Issues", example_list_issues),
        ("List Pull Requests", example_list_prs),
        ("Create Issue", example_create_issue),
        ("Create Pull Request", example_create_pr),
        ("Add Comments", example_comment),
        ("Update Issue/PR", example_update),
    ]
    
    for name, example_func in examples:
        print("\n" + "=" * 70)
        print(f"EXAMPLE: {name}")
        print("=" * 70 + "\n")
        try:
            await example_func()
        except Exception as e:
            print(f"Error: {e}")
        print("\n")
        await asyncio.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        examples = {
            "list_issues": example_list_issues,
            "list_prs": example_list_prs,
            "create_issue": example_create_issue,
            "create_pr": example_create_pr,
            "comment": example_comment,
            "update": example_update,
        }
        
        if example_name in examples:
            print(f"Running example: {example_name}")
            asyncio.run(examples[example_name]())
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(examples.keys())}")
    else:
        asyncio.run(run_all_examples())
