"""
Interactive demo for Branch Management tools

Usage:
    python examples/branch_management/interactive_demo.py
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
    print("GitHub MCP - Branch Management Demo")
    print("=" * 60)
    print("\nSelect an option:")
    print("  1. List Branches")
    print("  2. Create Branch (requires write access)")
    print("  3. Delete Branch (requires write access)")
    print("  4. Merge Branches (requires write access)")
    print("  5. Get Branch Protection")
    print("  6. Compare Branches")
    print("  0. Exit")
    print()


async def list_branches(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    protected_only = input("Protected branches only? (y/n): ").strip().lower() == 'y'
    
    print("\nFetching branches...")
    result = await session.call_tool(
        "list_branches",
        arguments={"owner": owner, "repo": repo, "protected_only": protected_only}
    )
    print_result(result)


async def create_branch(session):
    print("\n[NOTE] This requires write access to the repository.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    branch_name = input("New branch name: ").strip()
    from_branch = input("Create from branch (leave empty for default): ").strip() or None
    
    print("\nCreating branch...")
    args = {"owner": owner, "repo": repo, "branch_name": branch_name}
    if from_branch:
        args["from_branch"] = from_branch
    result = await session.call_tool("create_branch", arguments=args)
    print_result(result)


async def delete_branch(session):
    print("\n[NOTE] This requires write access to the repository.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    branch_name = input("Branch to delete: ").strip()
    
    confirm = input(f"Delete branch '{branch_name}'? (yes/no): ").strip()
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    print("\nDeleting branch...")
    result = await session.call_tool(
        "delete_branch",
        arguments={"owner": owner, "repo": repo, "branch_name": branch_name}
    )
    print_result(result)


async def merge_branches(session):
    print("\n[NOTE] This requires write access to the repository.")
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    base = input("Base branch (merge into): ").strip()
    head = input("Head branch (merge from): ").strip()
    message = input("Commit message (optional): ").strip() or None
    
    print("\nMerging branches...")
    args = {"owner": owner, "repo": repo, "base": base, "head": head}
    if message:
        args["commit_message"] = message
    result = await session.call_tool("merge_branches", arguments=args)
    print_result(result)


async def get_branch_protection(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    branch = input("Branch name (leave empty for default): ").strip() or None
    
    print("\nFetching protection rules...")
    args = {"owner": owner, "repo": repo}
    if branch:
        args["branch"] = branch
    result = await session.call_tool("get_branch_protection", arguments=args)
    print_result(result)


async def compare_branches(session):
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    base = input("Base branch: ").strip()
    head = input("Head branch: ").strip()
    
    print("\nComparing branches...")
    result = await session.call_tool(
        "compare_branches",
        arguments={"owner": owner, "repo": repo, "base": base, "head": head}
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
                    choice = input("Select an option (0-6): ").strip()
                    
                    if choice == "0":
                        print("\nGoodbye!")
                        break
                    elif choice == "1":
                        await list_branches(session)
                    elif choice == "2":
                        await create_branch(session)
                    elif choice == "3":
                        await delete_branch(session)
                    elif choice == "4":
                        await merge_branches(session)
                    elif choice == "5":
                        await get_branch_protection(session)
                    elif choice == "6":
                        await compare_branches(session)
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
