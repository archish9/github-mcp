"""
Interactive demo for Issues and Pull Requests tools

Usage:
    python examples/issues_and_prs/interactive_demo.py
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


def print_result(result):
    try:
        text = result.content[0].text
        data = json.loads(text)
        if isinstance(data, dict) and "error" in data:
            print("\n[ERROR]")
            print(f"  {data.get('message', data.get('error'))}")
        else:
            print("\n[RESULT]")
            print(json.dumps(data, indent=2))
    except:
        print(result.content[0].text)


def print_menu():
    print("\n" + "=" * 60)
    print("GitHub MCP - Issues and Pull Requests Demo")
    print("=" * 60)
    print("\nIssue Operations:")
    print("  1. List Issues")
    print("  2. Create Issue (requires write access)")
    print("  3. Add Issue Comment (requires write access)")
    print("  4. Close Issue (requires write access)")
    print("\nPull Request Operations:")
    print("  5. List Pull Requests")
    print("  6. Create Pull Request (requires write access)")
    print("  7. Add PR Comment (requires write access)")
    print("  8. Close Pull Request (requires write access)")
    print("\n  0. Exit")
    print()


async def list_issues(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    state = input("State (open/closed/all, default: open): ").strip() or "open"
    limit = input("Limit (default: 10): ").strip()
    limit = int(limit) if limit else 10
    
    print("\nFetching issues...")
    result = await session.call_tool(
        "list_issues",
        arguments={"owner": owner, "repo": repo, "state": state, "limit": limit}
    )
    print_result(result)


async def create_issue(session):
    print("\n[NOTE] Requires write access to the repository.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    title = input("Issue title: ").strip()
    body = input("Issue body: ").strip()
    labels = input("Labels (comma-separated, optional): ").strip()
    
    args = {"owner": owner, "repo": repo, "title": title, "body": body}
    if labels:
        args["labels"] = [l.strip() for l in labels.split(",")]
    
    print("\nCreating issue...")
    result = await session.call_tool("create_issue", arguments=args)
    print_result(result)


async def add_issue_comment(session):
    print("\n[NOTE] Requires write access.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    issue_number = int(input("Issue number: ").strip())
    body = input("Comment: ").strip()
    
    print("\nAdding comment...")
    result = await session.call_tool(
        "add_issue_comment",
        arguments={"owner": owner, "repo": repo, "issue_number": issue_number, "body": body}
    )
    print_result(result)


async def close_issue(session):
    print("\n[NOTE] Requires write access.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    issue_number = int(input("Issue number: ").strip())
    
    print("\nClosing issue...")
    result = await session.call_tool(
        "close_issue",
        arguments={"owner": owner, "repo": repo, "issue_number": issue_number}
    )
    print_result(result)


async def list_prs(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    state = input("State (open/closed/all, default: open): ").strip() or "open"
    limit = input("Limit (default: 10): ").strip()
    limit = int(limit) if limit else 10
    
    print("\nFetching pull requests...")
    result = await session.call_tool(
        "list_pull_requests",
        arguments={"owner": owner, "repo": repo, "state": state, "limit": limit}
    )
    print_result(result)


async def create_pr(session):
    print("\n[NOTE] Requires write access and existing branches.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    title = input("PR title: ").strip()
    body = input("PR body: ").strip()
    head = input("Head branch (to merge from): ").strip()
    base = input("Base branch (to merge into): ").strip()
    
    print("\nCreating pull request...")
    result = await session.call_tool(
        "create_pull_request",
        arguments={"owner": owner, "repo": repo, "title": title, "body": body, "head": head, "base": base}
    )
    print_result(result)


async def add_pr_comment(session):
    print("\n[NOTE] Requires write access.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    pr_number = int(input("PR number: ").strip())
    body = input("Comment: ").strip()
    
    print("\nAdding comment...")
    result = await session.call_tool(
        "add_pr_comment",
        arguments={"owner": owner, "repo": repo, "pr_number": pr_number, "body": body}
    )
    print_result(result)


async def close_pr(session):
    print("\n[NOTE] Requires write access.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    pr_number = int(input("PR number: ").strip())
    
    print("\nClosing pull request...")
    result = await session.call_tool(
        "close_pull_request",
        arguments={"owner": owner, "repo": repo, "pr_number": pr_number}
    )
    print_result(result)


async def main():
    print("Connecting to GitHub MCP server...")
    
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected!")
            
            while True:
                print_menu()
                try:
                    choice = input("Select an option (0-8): ").strip()
                    
                    if choice == "0":
                        print("\nGoodbye!")
                        break
                    elif choice == "1":
                        await list_issues(session)
                    elif choice == "2":
                        await create_issue(session)
                    elif choice == "3":
                        await add_issue_comment(session)
                    elif choice == "4":
                        await close_issue(session)
                    elif choice == "5":
                        await list_prs(session)
                    elif choice == "6":
                        await create_pr(session)
                    elif choice == "7":
                        await add_pr_comment(session)
                    elif choice == "8":
                        await close_pr(session)
                    else:
                        print("Invalid option.")
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\nError: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
