"""
Interactive demo for Commit History tools
Run this script and follow the menu prompts.

Usage:
    python examples/commit_history/interactive_demo.py
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
    """Pretty print JSON result"""
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
    print("GitHub MCP - Commit History Demo")
    print("=" * 60)
    print("\nSelect an option:")
    print("  1. List Commits")
    print("  2. Get Commit Details")
    print("  3. Search Commits")
    print("  4. Compare Commits/Branches")
    print("  5. Get Commit Statistics")
    print("  0. Exit")
    print()


async def list_commits(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    branch = input("Branch (leave empty for default): ").strip() or None
    limit = input("Number of commits (default: 10): ").strip()
    limit = int(limit) if limit else 10
    
    print("\nFetching commits...")
    args = {"owner": owner, "repo": repo, "limit": limit}
    if branch:
        args["branch"] = branch
    result = await session.call_tool("list_commits", arguments=args)
    print_result(result)


async def get_commit_details(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    sha = input("Commit SHA: ").strip()
    include_patch = input("Include patches? (y/n): ").strip().lower() == 'y'
    
    print("\nFetching commit details...")
    result = await session.call_tool(
        "get_commit_details",
        arguments={"owner": owner, "repo": repo, "sha": sha, "include_patch": include_patch}
    )
    print_result(result)


async def search_commits(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    author = input("Author (optional): ").strip() or None
    since = input("Since date YYYY-MM-DD (optional): ").strip() or None
    until = input("Until date YYYY-MM-DD (optional): ").strip() or None
    path = input("File path (optional): ").strip() or None
    limit = input("Limit (default: 10): ").strip()
    limit = int(limit) if limit else 10
    
    print("\nSearching commits...")
    args = {"owner": owner, "repo": repo, "limit": limit}
    if author:
        args["author"] = author
    if since:
        args["since"] = since
    if until:
        args["until"] = until
    if path:
        args["path"] = path
    result = await session.call_tool("search_commits", arguments=args)
    print_result(result)


async def compare_commits(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    base = input("Base (branch/tag/commit): ").strip()
    head = input("Head (branch/tag/commit): ").strip()
    
    print("\nComparing...")
    result = await session.call_tool(
        "compare_commits",
        arguments={"owner": owner, "repo": repo, "base": base, "head": head}
    )
    print_result(result)


async def get_commit_stats(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    days = input("Days to analyze (default: 30): ").strip()
    days = int(days) if days else 30
    
    print("\nFetching statistics...")
    result = await session.call_tool(
        "get_commit_stats",
        arguments={"owner": owner, "repo": repo, "days": days}
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
                    choice = input("Select an option (0-5): ").strip()
                    
                    if choice == "0":
                        print("\nGoodbye!")
                        break
                    elif choice == "1":
                        await list_commits(session)
                    elif choice == "2":
                        await get_commit_details(session)
                    elif choice == "3":
                        await search_commits(session)
                    elif choice == "4":
                        await compare_commits(session)
                    elif choice == "5":
                        await get_commit_stats(session)
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
